CREATE OR REPLACE FUNCTION demo.order_create(order_payload jsonb)
RETURNS jsonb AS $$
DECLARE
    inserted_order demo.orders%ROWTYPE;
    inserted_order_item demo.order_items%ROWTYPE;
    order_item_record jsonb;
    order_items_list jsonb := '[]'::jsonb;
BEGIN
    -- Create order header
    INSERT INTO demo.orders (customer_id, order_time)
    VALUES (
        (order_payload->>'customer_id')::BIGINT,
        (order_payload->>'order_time')::TIMESTAMPTZ
    )
    RETURNING * INTO inserted_order;

    -- Insert order items and decrement stock
    FOR order_item_record IN
        SELECT * FROM jsonb_array_elements(order_payload->'order_items')
    LOOP
        INSERT INTO demo.order_items (order_id, item_id, quantity, unit_price)
        VALUES (
            inserted_order.order_id,
            (order_item_record->>'item_id')::BIGINT,
            (order_item_record->>'quantity')::INT,
            (order_item_record->>'unit_price')::NUMERIC
        )
        RETURNING * INTO inserted_order_item;

        -- Add inserted item to JSON array
        order_items_list := order_items_list || to_jsonb(inserted_order_item);

        -- Decrement stock in items table
        UPDATE demo.items
        SET stock = stock - (order_item_record->>'quantity')::INT
        WHERE item_id = (order_item_record->>'item_id')::BIGINT;
    END LOOP;

    -- Return full order + items
       RETURN jsonb_build_object(
        'order_id', inserted_order.order_id,
        'customer_id', inserted_order.customer_id,
        'order_time', inserted_order.order_time,
        'order_items', COALESCE(order_items_list, '[]'::jsonb)
    );

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION demo.order_update(
    order_id_input BIGINT,
    order_items_payload JSONB
)
RETURNS JSONB AS $$
DECLARE
    order_item_record JSONB;
	cancelled_order_item_id BIGINT;
    existing_quantity INT;
    new_quantity INT;
    result JSONB;
BEGIN
    order_items_payload := order_items_payload->'order_items';

    -- Ensure order_items_payload is an array
    IF jsonb_typeof(order_items_payload) != 'array' THEN
        RAISE EXCEPTION 'order_items_payload must contain an "order_items" array';
    END IF;

    -- Restock deleted items
    FOR existing_quantity, cancelled_order_item_id IN
        SELECT order_items.quantity, order_items.item_id
        FROM demo.order_items
        WHERE order_items.order_id = order_id_input
          AND NOT EXISTS (
              SELECT 1
              FROM jsonb_array_elements(order_items_payload) AS elem
              WHERE (elem->>'item_id')::BIGINT = order_items.item_id
          )
    LOOP
        -- Restock cancelled order items by adding back the existing quantity
        UPDATE demo.items
        SET stock = stock + existing_quantity
        WHERE item_id = cancelled_order_item_id;

        -- Delete the order_item row
        DELETE FROM demo.order_items
        WHERE demo.order_items.order_id = order_id_input
          AND item_id = cancelled_order_item_id;
    END LOOP;

    -- For each provided item: update or insert
    FOR order_item_record IN
        SELECT * FROM jsonb_array_elements(order_items_payload)
    LOOP
        -- Check if item already exists
        SELECT quantity INTO existing_quantity
        FROM demo.order_items
        WHERE demo.order_items.order_id = order_id_input
          AND item_id = (order_item_record->>'item_id')::BIGINT;

        new_quantity := (order_item_record->>'quantity')::INT;

        IF FOUND THEN
            -- Adjust stock (add back old qty, subtract new qty)
            UPDATE demo.items
            SET stock = stock + existing_quantity - new_quantity
            WHERE item_id = (order_item_record->>'item_id')::BIGINT;

            -- Update existing order_item
            UPDATE demo.order_items
            SET quantity   = new_quantity,
                unit_price = (order_item_record->>'unit_price')::NUMERIC
            WHERE demo.order_items.order_id = order_id_input
              AND item_id = (order_item_record->>'item_id')::BIGINT;

        ELSE
            -- Insert new order_item
            INSERT INTO demo.order_items (order_id, item_id, quantity, unit_price)
            VALUES (
                order_id_input,
                (order_item_record->>'item_id')::BIGINT,
                new_quantity,
                (order_item_record->>'unit_price')::NUMERIC
            );

            -- Decrease stock for new item
            UPDATE demo.items
            SET stock = stock - new_quantity
            WHERE item_id = (order_item_record->>'item_id')::BIGINT;
        END IF;
    END LOOP;

    -- Build the result JSONB object
    SELECT jsonb_build_object(
        'order_id', o.order_id,
        'customer_id', o.customer_id,
        'order_time', o.order_time,
        'order_items', COALESCE((
            SELECT jsonb_agg(
                jsonb_build_object(
                    'order_item_id', oi.order_item_id,
                    'order_id', oi.order_id,
                    'item_id', oi.item_id,
                    'quantity', oi.quantity,
                    'unit_price', oi.unit_price
                )
            )
            FROM demo.order_items oi
            WHERE oi.order_id = order_id_input
        ), '[]'::jsonb)
    )
    INTO result
    FROM demo.orders o
    WHERE o.order_id = order_id_input;

    RETURN result;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION demo.order_delete(order_id_input BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    order_item_record RECORD;
    deleted_count INT;
BEGIN
    -- Restock items for the order being deleted
    FOR order_item_record IN
        SELECT item_id, quantity
        FROM demo.order_items
        WHERE order_id = order_id_input
    LOOP
        -- Increment stock for the item
        UPDATE demo.items
        SET stock = stock + order_item_record.quantity
        WHERE item_id = order_item_record.item_id;
    END LOOP;

    -- Delete all order items
    DELETE FROM demo.order_items
    WHERE order_id = order_id_input;

    -- Delete the order
    DELETE FROM demo.orders
    WHERE order_id = order_id_input;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;

    -- Return TRUE if the order was deleted, FALSE otherwise
    RETURN deleted_count > 0;
END;
$$ LANGUAGE plpgsql;

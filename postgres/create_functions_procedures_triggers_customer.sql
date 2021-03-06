DROP PROCEDURE IF EXISTS insert_creditcard;

CREATE OR REPLACE PROCEDURE insert_creditcard(p_card_number char, p_expiration_date char, p_name varchar) LANGUAGE plpgsql AS $$
	BEGIN 
		IF p_card_number ~ '^[0-9\.]{16}' AND p_expiration_date ~ '^[0-9\.]{4}' THEN 
			INSERT INTO credit_card(card_number, expiration_date, name) VALUES (p_card_number, p_expiration_date, p_name);
		END IF;
		RAISE NOTICE 'Cardnumber: % or expiration date: % is invalid', p_card_number, p_expiration_date;
	END
$$;
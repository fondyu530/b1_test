CREATE OR REPLACE PROCEDURE metrics(INOUT sum_int BIGINT, INOUT median_float DECIMAL)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
BEGIN
        SELECT SUM(int_number) INTO sum_int FROM rand_rows;
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY float_number) INTO median_float FROM rand_rows;
END;
$BODY$;

CALL metrics(NULL, NULL);

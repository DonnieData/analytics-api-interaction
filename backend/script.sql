select * from test_analytics.tabla_prueba;

select * from public."NY_Farmers_Markets";


ALTER TABLE public."NY_Farmers_Markets" 
ADD COLUMN id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY;
--------------------------------------------------------
-- Archivo creado  - jueves-mayo-12-2022   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Sequence COTIZACION_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "COTIZACION_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence DETALLE_SERVICIO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "DETALLE_SERVICIO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence DOCUMENTO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "DOCUMENTO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence GRUPO_PRODUCTO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "GRUPO_PRODUCTO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence MEDIO_PAGO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "MEDIO_PAGO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence ORDEN_PEDIDO_PRODUCTO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "ORDEN_PEDIDO_PRODUCTO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence RESERVA_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "RESERVA_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence SEQ_ERROR
--------------------------------------------------------

   CREATE SEQUENCE  "SEQ_ERROR"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 61 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence SEQ_IDSERVICIO
--------------------------------------------------------

   CREATE SEQUENCE  "SEQ_IDSERVICIO"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 41 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence SEQ_TIPO_EMP
--------------------------------------------------------

   CREATE SEQUENCE  "SEQ_TIPO_EMP"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 15 NOCACHE  ORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence SERVICIO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "SERVICIO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 21 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence TIPO_DOCUMENTO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "TIPO_DOCUMENTO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence TIPO_EMPLEADO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "TIPO_EMPLEADO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 21 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Sequence TIPO_PRODUCTO_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "TIPO_PRODUCTO_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL
--------------------------------------------------------
--  DDL for Trigger COTIZACION_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "COTIZACION_TRG" 
BEFORE INSERT ON COTIZACION 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.NUMERO_FOLIO IS NULL THEN
      SELECT COTIZACION_SEQ.NEXTVAL INTO :NEW.NUMERO_FOLIO FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "COTIZACION_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger DETALLE_SERVICIO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "DETALLE_SERVICIO_TRG" 
BEFORE INSERT ON DETALLE_SERVICIO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_DETALLE_SERVICIO IS NULL THEN
      SELECT DETALLE_SERVICIO_SEQ.NEXTVAL INTO :NEW.ID_DETALLE_SERVICIO FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "DETALLE_SERVICIO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger DOCUMENTO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "DOCUMENTO_TRG" 
BEFORE INSERT ON DOCUMENTO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_DOCUMENTO IS NULL THEN
      SELECT DOCUMENTO_SEQ.NEXTVAL INTO :NEW.ID_DOCUMENTO FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "DOCUMENTO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger GRUPO_PRODUCTO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "GRUPO_PRODUCTO_TRG" 
BEFORE INSERT ON GRUPO_PRODUCTO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_CATEGORIA IS NULL THEN
      SELECT GRUPO_PRODUCTO_SEQ.NEXTVAL INTO :NEW.ID_CATEGORIA FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "GRUPO_PRODUCTO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger LOG_ERROR_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "LOG_ERROR_TRG" 
BEFORE INSERT ON LOG_ERROR 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_ERROR IS NULL THEN
      SELECT SEQ_ERROR.NEXTVAL INTO :NEW.ID_ERROR FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "LOG_ERROR_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger MEDIO_PAGO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "MEDIO_PAGO_TRG" 
BEFORE INSERT ON MEDIO_PAGO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_PAGO IS NULL THEN
      SELECT MEDIO_PAGO_SEQ.NEXTVAL INTO :NEW.ID_PAGO FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "MEDIO_PAGO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger ORDEN_PEDIDO_PRODUCTO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "ORDEN_PEDIDO_PRODUCTO_TRG" 
BEFORE INSERT ON ORDEN_PEDIDO_PRODUCTO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.FOLIO_PEDIDO IS NULL THEN
      SELECT ORDEN_PEDIDO_PRODUCTO_SEQ.NEXTVAL INTO :NEW.FOLIO_PEDIDO FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "ORDEN_PEDIDO_PRODUCTO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger RESERVA_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "RESERVA_TRG" 
BEFORE INSERT ON RESERVA 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID IS NULL THEN
      SELECT RESERVA_SEQ.NEXTVAL INTO :NEW.ID FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "RESERVA_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger SERVICIO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "SERVICIO_TRG" 
BEFORE INSERT ON SERVICIO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_SEVICIO IS NULL THEN
      SELECT SERVICIO_SEQ.NEXTVAL INTO :NEW.ID_SEVICIO FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "SERVICIO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger TIPO_DOCUMENTO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "TIPO_DOCUMENTO_TRG" 
BEFORE INSERT ON TIPO_DOCUMENTO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_TIPO_DOC IS NULL THEN
      SELECT TIPO_DOCUMENTO_SEQ.NEXTVAL INTO :NEW.ID_TIPO_DOC FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "TIPO_DOCUMENTO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger TIPO_EMPLEADO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "TIPO_EMPLEADO_TRG" 
BEFORE INSERT ON TIPO_EMPLEADO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID_TIPO_EMP IS NULL THEN
      SELECT TIPO_EMPLEADO_SEQ.NEXTVAL INTO :NEW.ID_TIPO_EMP FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "TIPO_EMPLEADO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Trigger TIPO_PRODUCTO_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "TIPO_PRODUCTO_TRG" 
BEFORE INSERT ON TIPO_PRODUCTO 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.ID IS NULL THEN
      SELECT TIPO_PRODUCTO_SEQ.NEXTVAL INTO :NEW.ID FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "TIPO_PRODUCTO_TRG" ENABLE
--------------------------------------------------------
--  DDL for Procedure SP_AGREGAR_CLIENTE
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "SP_AGREGAR_CLIENTE" 
(
V_RUN IN CLIENTE.RUT_CLI%type, 
V_NOMBRE IN CLIENTE.NOMBRE%type, 
V_APELLIDO IN CLIENTE.APELLIDO%TYPE,
V_CONTACTO IN CLIENTE.CONTACTO%TYPE,
V_ACTIVO IN CLIENTE.ACTIVO%TYPE,
V_USERMAIL IN CLIENTE.USERMAIL%TYPE,
V_PASSWORD IN CLIENTE.PASSWORD%TYPE,
V_RUT_EMP IN CLIENTE.RUT_EMPRESA%TYPE,
V_GIRO IN CLIENTE.GIRO%TYPE,
V_RAZON IN CLIENTE.RAZON_SOCIAL%TYPE,

v_salida out number

)
is
begin
    --cursor con los rut de los clientes
    DECLARE
        CURSOR c_cliente IS
         SELECT RUT_CLI
         FROM CLIENTE;

        v_run_cliente CLIENTE.RUT_CLI%TYPE;

        confirmacion NUMBER;
    begin
        confirmacion := 0;
        for c in c_cliente loop
            v_run_cliente := c.rut_cli;
            --actualiza los datos del cliente
            --cuando el rut del cliente coincide
            if v_run_cliente = V_RUN THEN
                update cliente set
                    NOMBRE = V_NOMBRE,
                    APELLIDO = V_APELLIDO,
                    CONTACTO = V_CONTACTO,
                    USERMAIL = V_USERMAIL,
                    RUT_EMPRESA = V_RUT_EMP,
                    GIRO = V_GIRO,
                    RAZON_SOCIAL = V_RAZON
                where rut_cli = V_RUN;
                --actuliza los campos de accounts
                update ACCOUNTS_ACCOUNT set
                    FIRST_NAME = V_NOMBRE,
                    LAST_NAME = V_APELLIDO,
                    EMAIL = V_USERMAIL  
                where EMAIL = V_USERMAIL;
                confirmacion :=1;
            end if;
        end loop;
        --si no existe el cliente lo registra en la tabla
        if confirmacion != 1 then
            insert into cliente
            values(V_RUN,V_NOMBRE,V_APELLIDO,V_CONTACTO,V_ACTIVO,
                    V_USERMAIL,V_PASSWORD,V_RUT_EMP,V_GIRO,V_RAZON);
        end if;
    commit;
    end;
v_salida := 1;

exception
    when DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error de dato duplicado');
    WHEN OTHERS THEN 
        v_salida:=0;
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error desconocido');
end;
--------------------------------------------------------
--  DDL for Procedure SP_AGREGAR_SERVICIO
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SP_AGREGAR_SERVICIO" 
  (
v_name servicio.nombre%type,
v_precio servicio.precio%type,

v_salida out number

)
is
begin

insert into servicio
values(SEQ_IDSERVICIO.nextval,v_name,v_precio,1);
commit;

v_salida :=1;
exception
    when DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error de dato duplicado');
    WHEN OTHERS THEN 
        v_salida:=0;
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error desconocido');
END SP_AGREGAR_SERVICIO;
--------------------------------------------------------
--  DDL for Procedure SP_AGREGAR_TRABAJADOR
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "SP_AGREGAR_TRABAJADOR" 
(
V_RUN IN EMPLEADO.RUT_EMP%TYPE, 
V_NOMBRE IN EMPLEADO.NOMBRE%type, 
V_APELLIDO IN EMPLEADO.APELLIDOS%TYPE,
V_TELEFONO IN EMPLEADO.TELEFONO%TYPE,
V_ACTIVO IN EMPLEADO.ACTIVO%TYPE,
V_TIPO_EMP IN EMPLEADO.ID_TIPO_EMP%TYPE,
V_USERMAIL IN EMPLEADO.USERMAIL%TYPE,
V_PASSWORD IN EMPLEADO.PASSWORD%TYPE,


v_salida out number

)
is
begin
    --cursor con los rut de los clientes
    DECLARE
        CURSOR c_empleado IS
         SELECT RUT_EMP
         FROM EMPLEADO;

        v_run_empleado EMPLEADO.RUT_EMP%TYPE;

        confirmacion NUMBER;
    begin
        confirmacion := 0;
        for c in c_empleado loop
            v_run_empleado := c.rut_emp;
            --actualiza los datos del cliente
            --cuando el rut del cliente coincide
            if v_run_empleado = V_RUN THEN
                update empleado set
                    NOMBRE = V_NOMBRE,
                    APELLIDOS = V_APELLIDO,
                    TELEFONO = V_TELEFONO,
                    USERMAIL = V_USERMAIL
                where rut_emp = V_RUN;
                --actuliza los campos de accounts
                update ACCOUNTS_ACCOUNT set
                    FIRST_NAME = V_NOMBRE,
                    LAST_NAME = V_APELLIDO,
                    EMAIL = V_USERMAIL  
                where EMAIL = V_USERMAIL;
                confirmacion :=1;
            end if;
        end loop;
        --si no existe el cliente lo registra en la tabla
        if confirmacion != 1 then
            insert into empleado
            values(V_RUN,V_NOMBRE,V_APELLIDO,V_TELEFONO,V_ACTIVO,V_TIPO_EMP,
                    V_USERMAIL,V_PASSWORD);
        end if;
    commit;
    end;
v_salida := 1;

exception
    when DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error de dato duplicado');
    WHEN OTHERS THEN 
        v_salida:=0;
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error desconocido');
end;
--------------------------------------------------------
--  DDL for Procedure SP_LISTA_TIPO_EMPLEADO
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "SP_LISTA_TIPO_EMPLEADO" 
(REG OUT SYS_REFCURSOR)
AS

BEGIN
OPEN REG FOR 
SELECT id_tipo_emp, seccion FROM tipo_empleado;
END;
--------------------------------------------------------
--  DDL for Procedure SP_TIPO_EMPLEADO
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "SP_TIPO_EMPLEADO" 
(
v_seccion tipo_empleado.seccion%type,

v_salida out number

)
is
begin

insert into tipo_empleado
values(SEQ_TIPO_EMP.nextval,v_seccion);
commit;

v_salida :=1;
exception
    when DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error de dato duplicado');
    WHEN OTHERS THEN 
        v_salida:=0;
        RAISE_APPLICATION_ERROR(SEQ_ERROR.NEXTVAL,' Error desconocido');
end;

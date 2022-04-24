DROP TABLE cliente CASCADE CONSTRAINTS;

DROP TABLE cotizacion CASCADE CONSTRAINTS;

DROP TABLE detalle_documento CASCADE CONSTRAINTS;

DROP TABLE detalle_servicio CASCADE CONSTRAINTS;

DROP TABLE documento CASCADE CONSTRAINTS;

DROP TABLE empleado CASCADE CONSTRAINTS;

DROP TABLE grupo_producto CASCADE CONSTRAINTS;

DROP TABLE medio_pago CASCADE CONSTRAINTS;

DROP TABLE orden_pedido_producto CASCADE CONSTRAINTS;

DROP TABLE "ORDEN-PRODUCTO" CASCADE CONSTRAINTS;

DROP TABLE producto CASCADE CONSTRAINTS;

DROP TABLE proveedor CASCADE CONSTRAINTS;

DROP TABLE "PROV-PRODUCTO" CASCADE CONSTRAINTS;

DROP TABLE reserva CASCADE CONSTRAINTS;

DROP TABLE servicio CASCADE CONSTRAINTS;

DROP TABLE tipo_documento CASCADE CONSTRAINTS;

DROP TABLE tipo_empleado CASCADE CONSTRAINTS;

DROP TABLE tipo_producto CASCADE CONSTRAINTS;

DROP TABLE vehiculo CASCADE CONSTRAINTS;


CREATE TABLE cliente (
    rut_cli      VARCHAR2(10) NOT NULL,
    nombre       VARCHAR2(30) NOT NULL,
    apellido     VARCHAR2(30) NOT NULL,
    contacto     NUMBER(9),
    activo       NUMBER NOT NULL,
    usermail     VARCHAR2(100) NOT NULL,
    password     VARCHAR2(300) NOT NULL,
    rut_empresa  VARCHAR2(10),
    giro         VARCHAR2(50),
    razon_social VARCHAR2(50)
);

ALTER TABLE cliente ADD CONSTRAINT cliente_pk PRIMARY KEY ( rut_cli );

CREATE TABLE cotizacion (
    numero_folio NUMBER(9) NOT NULL,
    comentario   VARCHAR2(300) NOT NULL,
    reserva_id   NUMBER(9) NOT NULL,
    id_sevicio   NUMBER(9) NOT NULL,
    valor        NUMBER(9) NOT NULL
);

ALTER TABLE cotizacion ADD CONSTRAINT cotizacion_pk PRIMARY KEY ( numero_folio );

CREATE TABLE detalle_documento (
    servicio_id_sevicio    NUMBER(9) NOT NULL,
    documento_id_documento NUMBER(9) NOT NULL
);

ALTER TABLE detalle_documento ADD CONSTRAINT detalle_documento_pk PRIMARY KEY ( servicio_id_sevicio,
                                                                                documento_id_documento );

CREATE TABLE detalle_servicio (
    id_detalle_servicio NUMBER(9) NOT NULL,
    cantidad            NUMBER(2) NOT NULL,
    servicio_id_sevicio NUMBER(9) NOT NULL,
    producto_sku        NUMBER(9) NOT NULL
);

ALTER TABLE detalle_servicio
    ADD CONSTRAINT detalle_servicio_pk PRIMARY KEY ( producto_sku,
                                                     servicio_id_sevicio,
                                                     id_detalle_servicio );

CREATE TABLE documento (
    id_documento  NUMBER(9) NOT NULL,
    folio         NUMBER(9) NOT NULL,
    fecha_emision DATE NOT NULL,
    total         NUMBER(9) NOT NULL,
    nulo          NUMBER NOT NULL,
    id_tipo_doc   NUMBER(9) NOT NULL,
    rut_emp       VARCHAR2(10) NOT NULL,
    rut_cli       VARCHAR2(10) NOT NULL,
    id_pago       NUMBER(9) NOT NULL,
    descuento     NUMBER(9)
);

ALTER TABLE documento ADD CONSTRAINT documento_pk PRIMARY KEY ( id_documento );

CREATE TABLE empleado (
    rut_emp     VARCHAR2(10) NOT NULL,
    nombre      VARCHAR2(30) NOT NULL,
    apellidos   VARCHAR2(50) NOT NULL,
    telefono    NUMBER(9) NOT NULL,
    activo      NUMBER NOT NULL,
    id_tipo_emp NUMBER(9) NOT NULL,
    usermail    VARCHAR2(100) NOT NULL,
    password    VARCHAR2(300) NOT NULL
);

ALTER TABLE empleado ADD CONSTRAINT empleado_pk PRIMARY KEY ( rut_emp );

CREATE TABLE grupo_producto (
    id_categoria     NUMBER(9) NOT NULL,
    nombre           VARCHAR2(25) NOT NULL,
    tipo_producto_id NUMBER(9) NOT NULL
);

ALTER TABLE grupo_producto ADD CONSTRAINT grupo_producto_pk PRIMARY KEY ( id_categoria );

CREATE TABLE medio_pago (
    id_pago NUMBER(9) NOT NULL,
    nombre  VARCHAR2(50) NOT NULL,
    enuso   NUMBER NOT NULL
);

ALTER TABLE medio_pago ADD CONSTRAINT medio_pago_pk PRIMARY KEY ( id_pago );

CREATE TABLE orden_pedido_producto (
    folio_pedido    NUMBER(9) NOT NULL,
    cantidad        NUMBER(9) NOT NULL,
    fecha_emision   DATE NOT NULL,
    recibido        NUMBER NOT NULL,
    fecha_recepcion DATE,
    rut_proveedor   VARCHAR2(10) NOT NULL
);

ALTER TABLE orden_pedido_producto ADD CONSTRAINT orden_pedido_producto_pk PRIMARY KEY ( folio_pedido );

CREATE TABLE "ORDEN-PRODUCTO" (
    sku_fk          NUMBER(9) NOT NULL,
    folio_pedido_fk NUMBER(9) NOT NULL
);

ALTER TABLE "ORDEN-PRODUCTO" ADD CONSTRAINT relation_19_pk PRIMARY KEY ( sku_fk,
                                                                         folio_pedido_fk );

CREATE TABLE producto (
    sku               NUMBER(9) NOT NULL,
    nombre_corto      VARCHAR2(30) NOT NULL,
    descripcion       VARCHAR2(200) NOT NULL,
    precio_compra     NUMBER(9) NOT NULL,
    precio_venta      NUMBER(9) NOT NULL,
    stock             NUMBER(9) NOT NULL,
    stock_critico     NUMBER(9) NOT NULL,
    enuso             NUMBER NOT NULL,
    id_categoria      NUMBER(9) NOT NULL,
    fecha_vencimiento DATE,
    unidad_medida     VARCHAR2(50) NOT NULL
);

ALTER TABLE producto ADD CONSTRAINT producto_pk PRIMARY KEY ( sku );

CREATE TABLE proveedor (
    rut_proveedor VARCHAR2(10) NOT NULL,
    nombre        VARCHAR2(100) NOT NULL,
    correo        VARCHAR2(50) NOT NULL
);

ALTER TABLE proveedor ADD CONSTRAINT proveedor_pk PRIMARY KEY ( rut_proveedor );

CREATE TABLE "PROV-PRODUCTO" (
    rut_proveedor VARCHAR2(10) NOT NULL,
    sku           NUMBER(9) NOT NULL
);

ALTER TABLE "PROV-PRODUCTO" ADD CONSTRAINT relation_5_pk PRIMARY KEY ( rut_proveedor,
                                                                       sku );

CREATE TABLE reserva (
    id              NUMBER(9) NOT NULL,
    fecha           DATE NOT NULL,
    estado          NUMBER NOT NULL,
    cliente_rut_cli VARCHAR2(10) NOT NULL
);

ALTER TABLE reserva ADD CONSTRAINT reserva_pk PRIMARY KEY ( id );

CREATE TABLE servicio (
    id_sevicio NUMBER(9) NOT NULL,
    nombre     VARCHAR2(35) NOT NULL,
    precio     NUMBER(9) NOT NULL,
    enuso      NUMBER NOT NULL
);

ALTER TABLE servicio ADD CONSTRAINT servicio_pk PRIMARY KEY ( id_sevicio );

CREATE TABLE tipo_documento (
    id_tipo_doc NUMBER(9) NOT NULL,
    nombre      VARCHAR2(20) NOT NULL
);

ALTER TABLE tipo_documento ADD CONSTRAINT tipo_documento_pk PRIMARY KEY ( id_tipo_doc );

CREATE TABLE tipo_empleado (
    id_tipo_emp NUMBER(9) NOT NULL,
    seccion     VARCHAR2(35) NOT NULL
);

ALTER TABLE tipo_empleado ADD CONSTRAINT tipo_empleado_pk PRIMARY KEY ( id_tipo_emp );

CREATE TABLE tipo_producto (
    id     NUMBER(9) NOT NULL,
    nombre VARCHAR2(45) NOT NULL
);

ALTER TABLE tipo_producto ADD CONSTRAINT tipo_producto_pk PRIMARY KEY ( id );

CREATE TABLE vehiculo (
    pantente        VARCHAR2(6) NOT NULL,
    marca           VARCHAR2(30) NOT NULL,
    modelo          VARCHAR2(30) NOT NULL,
    anio            NUMBER(4) NOT NULL,
    activo          NUMBER NOT NULL,
    cliente_rut_cli VARCHAR2(10) NOT NULL
);

ALTER TABLE vehiculo ADD CONSTRAINT vehiculo_pk PRIMARY KEY ( pantente );

ALTER TABLE cotizacion
    ADD CONSTRAINT cotizacion_reserva_fk FOREIGN KEY ( reserva_id )
        REFERENCES reserva ( id );

ALTER TABLE cotizacion
    ADD CONSTRAINT cotizacion_servicio_fk FOREIGN KEY ( id_sevicio )
        REFERENCES servicio ( id_sevicio );

ALTER TABLE detalle_documento
    ADD CONSTRAINT detalle_documento_documento_fk FOREIGN KEY ( documento_id_documento )
        REFERENCES documento ( id_documento );

ALTER TABLE detalle_documento
    ADD CONSTRAINT detalle_documento_servicio_fk FOREIGN KEY ( servicio_id_sevicio )
        REFERENCES servicio ( id_sevicio );

ALTER TABLE detalle_servicio
    ADD CONSTRAINT detalle_servicio_producto_fk FOREIGN KEY ( producto_sku )
        REFERENCES producto ( sku );

ALTER TABLE detalle_servicio
    ADD CONSTRAINT detalle_servicio_servicio_fk FOREIGN KEY ( servicio_id_sevicio )
        REFERENCES servicio ( id_sevicio );

ALTER TABLE documento
    ADD CONSTRAINT documento_cliente_fk FOREIGN KEY ( rut_cli )
        REFERENCES cliente ( rut_cli );

ALTER TABLE documento
    ADD CONSTRAINT documento_empleado_fk FOREIGN KEY ( rut_emp )
        REFERENCES empleado ( rut_emp );

ALTER TABLE documento
    ADD CONSTRAINT documento_medio_pago_fk FOREIGN KEY ( id_pago )
        REFERENCES medio_pago ( id_pago );

ALTER TABLE documento
    ADD CONSTRAINT documento_tipo_documento_fk FOREIGN KEY ( id_tipo_doc )
        REFERENCES tipo_documento ( id_tipo_doc );

ALTER TABLE empleado
    ADD CONSTRAINT empleado_tipo_empleado_fk FOREIGN KEY ( id_tipo_emp )
        REFERENCES tipo_empleado ( id_tipo_emp );

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE grupo_producto
    ADD CONSTRAINT tipo_producto_fk FOREIGN KEY ( tipo_producto_id )
        REFERENCES tipo_producto ( id );

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE orden_pedido_producto
    ADD CONSTRAINT producto_proveedor_fk FOREIGN KEY ( rut_proveedor )
        REFERENCES proveedor ( rut_proveedor );

ALTER TABLE producto
    ADD CONSTRAINT producto_grupo_producto_fk FOREIGN KEY ( id_categoria )
        REFERENCES grupo_producto ( id_categoria );
 
ALTER TABLE "ORDEN-PRODUCTO"
    ADD CONSTRAINT pedido_producto_fk FOREIGN KEY ( folio_pedido_fk )
        REFERENCES orden_pedido_producto ( folio_pedido );

ALTER TABLE "ORDEN-PRODUCTO"
    ADD CONSTRAINT relation_19_producto_fk FOREIGN KEY ( sku_fk )
        REFERENCES producto ( sku );

ALTER TABLE "PROV-PRODUCTO"
    ADD CONSTRAINT relation_5_producto_fk FOREIGN KEY ( sku )
        REFERENCES producto ( sku );

ALTER TABLE "PROV-PRODUCTO"
    ADD CONSTRAINT relation_5_proveedor_fk FOREIGN KEY ( rut_proveedor )
        REFERENCES proveedor ( rut_proveedor );

ALTER TABLE reserva
    ADD CONSTRAINT reserva_cliente_fk FOREIGN KEY ( cliente_rut_cli )
        REFERENCES cliente ( rut_cli );

ALTER TABLE vehiculo
    ADD CONSTRAINT vehiculo_cliente_fk FOREIGN KEY ( cliente_rut_cli )
        REFERENCES cliente ( rut_cli );

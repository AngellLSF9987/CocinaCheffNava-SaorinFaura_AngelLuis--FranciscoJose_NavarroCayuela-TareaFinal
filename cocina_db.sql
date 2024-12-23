-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-12-2024 a las 15:11:32
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cocina_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id_carrito` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `id_producto_FK` int(11) DEFAULT NULL,
  `id_cliente_FK` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito_productos`
--

CREATE TABLE `carrito_productos` (
  `id_carrito_FK` int(11) NOT NULL,
  `id_producto_FK` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre_categoria` varchar(255) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre_categoria`, `descripcion`, `imagen`) VALUES
(1, 'Carnes', 'Carnes a la parrilla y guisos de carne.', 'carnes.png'),
(2, 'Pastas', 'Platos de pasta italiana y fideos.', 'pastas.png'),
(3, 'Comidas de Puchero', 'Platos tradicionales de puchero.', 'puchero.png'),
(4, 'Pizzas', 'Pizzas artesanales con ingredientes frescos.', 'pizzas.png'),
(5, 'Arroces', 'Platos de arroz como paellas y risottos.', 'arroces.png'),
(6, 'Asados', 'Carnes y vegetales asados al horno.', 'asados.png'),
(7, 'Ensaladas', 'Ensaladas frescas y saludables.', 'ensaladas.png'),
(8, 'Cervezas', 'Cervezas nacionales e internacionales.', 'cervezas.png'),
(9, 'Vinos', 'Selección de vinos tintos, blancos y rosados.', 'vinos.png'),
(10, 'Refrescos con Gas y Sin Gas', 'Refrescos variados con y sin gas.', 'refrescos.png'),
(11, 'Aguas, zumos y batidos', 'Aguas minerales, zumos naturales y batidos.', 'bebidas.png'),
(12, 'Postres', 'Dulces y postres caseros.', 'postres.png'),
(13, 'Cafés', 'Cafés calientes y fríos.', 'cafes.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre_cliente` varchar(255) NOT NULL,
  `apellido1` varchar(255) NOT NULL,
  `apellido2` varchar(255) NOT NULL,
  `dni_cliente` varchar(9) NOT NULL,
  `telefono` varchar(9) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `id_usuario_FK` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre_cliente`, `apellido1`, `apellido2`, `dni_cliente`, `telefono`, `direccion`, `email`, `id_usuario_FK`) VALUES
(1, 'Francisco José', 'Cayuela', 'Navarro', '12345678A', '600123456', 'Calle Luna, 6', 'paco@nava.com', 1),
(2, 'Angel Luis', 'Saorin', 'Faura', '12345678C', '610654321', 'Calle Sol, 8', 'angel@saorin.com', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `num_pedido` int(11) DEFAULT NULL,
  `id_carrito_FK` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_carrito` decimal(10,2) DEFAULT NULL,
  `fecha_pedido` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre_producto` text DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `id_categoria_FK` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre_producto`, `descripcion`, `precio`, `imagen`, `id_categoria_FK`) VALUES
(1, 'Entrecot', 'Entrecot a la parrilla con guarnición de papas.', 15.99, 'entrecot.png', 1),
(2, 'Albóndigas en Salsa', 'Albóndigas de carne en salsa casera.', 9.50, 'albondigas.png', 1),
(3, 'Espaguetis Carbonara', 'Espaguetis con salsa carbonara casera.', 8.99, 'spagueti_carbonara.png', 2),
(4, 'Lasaña de Verduras', 'Lasaña vegetariana con capas de verduras frescas.', 9.75, 'lasana_verduras.png', 2),
(5, 'Cocido Madrileño', 'Cocido con garbanzos, carne y verduras.', 12.50, 'cocido.png', 3),
(6, 'Lentejas con Chorizo', 'Lentejas guisadas con chorizo.', 10.00, 'lentejas.png', 3),
(7, 'Pizza Margarita', 'Pizza clásica con tomate, queso y albahaca.', 7.99, 'margarita.png', 4),
(8, 'Pizza 4 Quesos', 'Pizza con mezcla de cuatro quesos italianos.', 9.50, '4quesos.png', 4),
(9, 'Paella de Marisco', 'Paella de mariscos recién preparada.', 13.99, 'paella_marisco.png', 5),
(10, 'Risotto de Setas', 'Risotto cremoso con setas variadas.', 11.50, 'risotto.png', 5),
(11, 'Pollo Asado', 'Pollo asado al horno con especias.', 12.00, 'pollo_asado.png', 6),
(12, 'Costillas BBQ', 'Costillas al horno con salsa barbacoa.', 14.00, 'costillas.png', 6),
(13, 'Ensalada César', 'Ensalada con pollo, crutones y aderezo César.', 7.50, 'ensalada_cesar.png', 7),
(14, 'Ensalada Mediterránea', 'Ensalada fresca con aceitunas, queso feta y tomate.', 6.99, 'ensalada_med.png', 7),
(15, 'Cerveza Lager', 'Botella de cerveza lager 330ml.', 2.50, 'cerveza_lager.png', 8),
(16, 'Cerveza IPA', 'Botella de cerveza IPA artesanal 330ml.', 3.00, 'cerveza_ipa.png', 8),
(17, 'Vino Tinto', 'Copa de vino tinto de la casa.', 3.50, 'vino_tinto.png', 9),
(18, 'Vino Blanco', 'Copa de vino blanco fresco.', 3.50, 'vino_blanco.png', 9),
(19, 'Coca-Cola', 'Refresco de cola original 330ml.', 1.80, 'coca_cola.png', 10),
(20, 'Limonada', 'Refresco de limón natural sin gas.', 1.50, 'fanta_limon.png', 10),
(21, 'Agua Mineral', 'Botella de agua mineral 500ml.', 1.20, 'aguapet.png', 11),
(22, 'Batido de Fresa', 'Batido natural de fresa con leche.', 2.50, 'batido_fresa.png', 11),
(23, 'Tarta de Manzana', 'Tarta de manzana casera con canela.', 4.50, 'tarta_manzana.png', 12),
(24, 'Flan Casero', 'Flan de huevo hecho en casa.', 3.50, 'flan.png', 12),
(25, 'Café Solo', 'Café espresso recién hecho.', 1.50, 'cafe_solo.png', 13),
(26, 'Café con Leche', 'Café con leche espumosa.', 1.80, 'cafe_leche.png', 13);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre_rol`) VALUES
(1, 'cliente'),
(2, 'trabajador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajadores`
--

CREATE TABLE `trabajadores` (
  `id_trabajador` int(11) NOT NULL,
  `nombre_trabajador` varchar(255) NOT NULL,
  `apellido1` varchar(255) NOT NULL,
  `apellido2` varchar(255) NOT NULL,
  `dni_trabajador` varchar(9) NOT NULL,
  `telefono` varchar(9) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `id_usuario_FK` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `trabajadores`
--

INSERT INTO `trabajadores` (`id_trabajador`, `nombre_trabajador`, `apellido1`, `apellido2`, `dni_trabajador`, `telefono`, `direccion`, `email`, `id_usuario_FK`) VALUES
(1, 'Paco', 'Lopez', 'Garcia', '12345678D', '620987654', 'Calle Estrella, 10', 'paco@trabajador.com', 3),
(2, 'Angel', 'Martinez', 'Perez', '12345678F', '630456789', 'Calle Cometa, 12', 'angel@trabajador.com', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `fecha_registro` date DEFAULT curdate(),
  `id_rol_FK` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `email`, `contraseña`, `fecha_registro`, `id_rol_FK`) VALUES
(1, 'paco@nava.com', 'paco123', '2024-12-23', 1),
(2, 'angel@saorin.com', 'angel123', '2024-12-23', 1),
(3, 'paco@trabajador.com', 'paco456', '2024-12-23', 2),
(4, 'angel@trabajador.com', 'angel456', '2024-12-23', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id_carrito`),
  ADD KEY `id_producto_FK` (`id_producto_FK`),
  ADD KEY `id_cliente_FK` (`id_cliente_FK`);

--
-- Indices de la tabla `carrito_productos`
--
ALTER TABLE `carrito_productos`
  ADD PRIMARY KEY (`id_carrito_FK`,`id_producto_FK`),
  ADD KEY `id_producto_FK` (`id_producto_FK`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `dni_cliente` (`dni_cliente`),
  ADD KEY `id_usuario_FK` (`id_usuario_FK`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_carrito_FK` (`id_carrito_FK`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_categoria_FK` (`id_categoria_FK`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`),
  ADD UNIQUE KEY `nombre_rol` (`nombre_rol`);

--
-- Indices de la tabla `trabajadores`
--
ALTER TABLE `trabajadores`
  ADD PRIMARY KEY (`id_trabajador`),
  ADD UNIQUE KEY `dni_trabajador` (`dni_trabajador`),
  ADD KEY `id_usuario_FK` (`id_usuario_FK`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `contraseña` (`contraseña`),
  ADD KEY `id_rol_FK` (`id_rol_FK`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id_carrito` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `trabajadores`
--
ALTER TABLE `trabajadores`
  MODIFY `id_trabajador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`id_producto_FK`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`id_cliente_FK`) REFERENCES `clientes` (`id_cliente`);

--
-- Filtros para la tabla `carrito_productos`
--
ALTER TABLE `carrito_productos`
  ADD CONSTRAINT `carrito_productos_ibfk_1` FOREIGN KEY (`id_carrito_FK`) REFERENCES `carrito` (`id_carrito`) ON DELETE CASCADE,
  ADD CONSTRAINT `carrito_productos_ibfk_2` FOREIGN KEY (`id_producto_FK`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_usuario_FK`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_carrito_FK`) REFERENCES `carrito` (`id_carrito`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria_FK`) REFERENCES `categorias` (`id_categoria`);

--
-- Filtros para la tabla `trabajadores`
--
ALTER TABLE `trabajadores`
  ADD CONSTRAINT `trabajadores_ibfk_1` FOREIGN KEY (`id_usuario_FK`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol_FK`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

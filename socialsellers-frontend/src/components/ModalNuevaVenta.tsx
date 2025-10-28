import { useState, useEffect } from 'react';
import Modal from './ui/Modal';
import Button from './ui/Button';
import Input from './ui/Input';
import { productosAPI, vendedoresAPI, ventasAPI } from '../services/api';
import type { Producto, Usuario } from '../types';

interface ModalNuevaVentaProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function ModalNuevaVenta({ isOpen, onClose, onSuccess }: ModalNuevaVentaProps) {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [vendedores, setVendedores] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Form state
  const [productoId, setProductoId] = useState('');
  const [vendedorId, setVendedorId] = useState('');
  const [cantidad, setCantidad] = useState('1');
  const [precioUnitario, setPrecioUnitario] = useState('');

  // Cargar productos y vendedores al abrir el modal
  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  const loadData = async () => {
    try {
      const [productosData, vendedoresData] = await Promise.all([
        productosAPI.getAll(),
        vendedoresAPI.getAll(),
      ]);
      setProductos(productosData);
      setVendedores(vendedoresData);
    } catch (err) {
      setError('Error al cargar datos');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await ventasAPI.createAdmin({
        producto_id: parseInt(productoId),
        vendedor_id: parseInt(vendedorId),
        cantidad: parseInt(cantidad),
        precio_unitario: parseFloat(precioUnitario),
      });

      // Resetear form
      setProductoId('');
      setVendedorId('');
      setCantidad('1');
      setPrecioUnitario('');

      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al crear venta');
    } finally {
      setLoading(false);
    }
  };

  // Auto-completar precio unitario cuando se selecciona un producto
  const handleProductoChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedId = e.target.value;
    setProductoId(selectedId);

    if (selectedId) {
      const producto = productos.find((p) => p.id === parseInt(selectedId));
      if (producto) {
        setPrecioUnitario(producto.precio_venta.toString());
      }
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Registrar Nueva Venta">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Producto */}
        <div>
          <label htmlFor="producto" className="block text-sm font-medium text-gray-700 mb-1">
            Producto *
          </label>
          <select
            id="producto"
            value={productoId}
            onChange={handleProductoChange}
            required
            disabled={loading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Seleccionar producto"
          >
            <option value="">Seleccionar producto...</option>
            {productos.map((producto) => (
              <option key={producto.id} value={producto.id}>
                {producto.nombre} - ${producto.precio_venta}
              </option>
            ))}
          </select>
        </div>

        {/* Vendedor */}
        <div>
          <label htmlFor="vendedor" className="block text-sm font-medium text-gray-700 mb-1">
            Vendedor *
          </label>
          <select
            id="vendedor"
            value={vendedorId}
            onChange={(e) => setVendedorId(e.target.value)}
            required
            disabled={loading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Seleccionar vendedor"
          >
            <option value="">Seleccionar vendedor...</option>
            {vendedores
              .filter((v) => v.rol === 'vendedor')
              .map((vendedor) => (
                <option key={vendedor.id} value={vendedor.id}>
                  {vendedor.nombre}
                </option>
              ))}
          </select>
        </div>

        {/* Cantidad */}
        <div>
          <label htmlFor="cantidad" className="block text-sm font-medium text-gray-700 mb-1">
            Cantidad *
          </label>
          <Input
            id="cantidad"
            type="number"
            min="1"
            value={cantidad}
            onChange={(e) => setCantidad(e.target.value)}
            required
            disabled={loading}
            aria-label="Cantidad"
          />
        </div>

        {/* Precio Unitario */}
        <div>
          <label htmlFor="precioUnitario" className="block text-sm font-medium text-gray-700 mb-1">
            Precio Unitario *
          </label>
          <Input
            id="precioUnitario"
            type="number"
            step="0.01"
            min="0.01"
            value={precioUnitario}
            onChange={(e) => setPrecioUnitario(e.target.value)}
            required
            disabled={loading}
            aria-label="Precio unitario"
          />
        </div>

        {/* Total calculado */}
        {precioUnitario && cantidad && (
          <div className="bg-gray-50 p-3 rounded-md">
            <p className="text-sm text-gray-600">
              Total:{' '}
              <span className="font-semibold text-gray-900">
                ${(parseFloat(precioUnitario) * parseInt(cantidad || '0')).toFixed(2)}
              </span>
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm">
            {error}
          </div>
        )}

        {/* Botones */}
        <div className="flex gap-3 justify-end pt-2">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={loading}
          >
            Cancelar
          </Button>
          <Button
            type="submit"
            disabled={loading}
            aria-label="Guardar venta"
          >
            {loading ? 'Guardando...' : 'Guardar'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}

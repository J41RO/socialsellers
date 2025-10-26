import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { ventasAPI, productosAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import type { Venta, Producto, VentaCreate } from '../types';
import { Plus } from 'lucide-react';

export default function Ventas() {
  const { usuario } = useAuth();
  const [ventas, setVentas] = useState<Venta[]>([]);
  const [productos, setProductos] = useState<Producto[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<VentaCreate>({
    producto_id: 0,
    cantidad: 1,
    precio_unitario: 0,
  });

  useEffect(() => {
    cargarDatos();
  }, [usuario]);

  const cargarDatos = async () => {
    try {
      const productosData = await productosAPI.getAll();
      setProductos(productosData.filter(p => p.activo && p.stock_actual > 0));

      const ventasData = usuario?.rol === 'admin'
        ? await ventasAPI.getAll()
        : await ventasAPI.getByVendedor(usuario?.id || 0);
      setVentas(ventasData);
    } catch (error) {
      console.error('Error al cargar datos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProductoChange = (productoId: number) => {
    const producto = productos.find(p => p.id === productoId);
    if (producto) {
      setFormData({
        ...formData,
        producto_id: productoId,
        precio_unitario: producto.precio_venta,
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ventasAPI.create(formData);
      resetForm();
      cargarDatos();
      alert('Venta registrada exitosamente');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al registrar venta');
    }
  };

  const resetForm = () => {
    setFormData({
      producto_id: 0,
      cantidad: 1,
      precio_unitario: 0,
    });
    setShowForm(false);
  };

  const productoSeleccionado = productos.find(p => p.id === formData.producto_id);
  const totalVenta = formData.cantidad * formData.precio_unitario;
  const comisionEstimada = usuario?.comision_porcentaje
    ? (totalVenta * usuario.comision_porcentaje) / 100
    : 0;

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-lg">Cargando...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="px-4 sm:px-0">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Registro de Ventas</h2>
          <Button onClick={() => setShowForm(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Nueva Venta
          </Button>
        </div>

        {showForm && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Registrar Nueva Venta</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Producto</label>
                  <select
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={formData.producto_id}
                    onChange={(e) => handleProductoChange(parseInt(e.target.value))}
                    required
                  >
                    <option value={0}>Seleccionar producto...</option>
                    {productos.map((producto) => (
                      <option key={producto.id} value={producto.id}>
                        {producto.nombre} - ${producto.precio_venta.toFixed(2)} (Stock: {producto.stock_actual})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Cantidad</label>
                  <Input
                    type="number"
                    min="1"
                    max={productoSeleccionado?.stock_actual || 999}
                    value={formData.cantidad}
                    onChange={(e) =>
                      setFormData({ ...formData, cantidad: parseInt(e.target.value) })
                    }
                    required
                  />
                  {productoSeleccionado && (
                    <p className="text-xs text-gray-500 mt-1">
                      Stock disponible: {productoSeleccionado.stock_actual}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Precio Unitario</label>
                  <Input
                    type="number"
                    step="0.01"
                    value={formData.precio_unitario}
                    onChange={(e) =>
                      setFormData({ ...formData, precio_unitario: parseFloat(e.target.value) })
                    }
                    required
                  />
                </div>

                {formData.producto_id > 0 && (
                  <div className="bg-gray-50 p-4 rounded-md space-y-2">
                    <div className="flex justify-between">
                      <span className="font-medium">Total Venta:</span>
                      <span className="font-bold">${totalVenta.toFixed(2)}</span>
                    </div>
                    {usuario?.rol === 'vendedor' && (
                      <div className="flex justify-between text-green-600">
                        <span className="font-medium">Tu Comisión ({usuario.comision_porcentaje}%):</span>
                        <span className="font-bold">${comisionEstimada.toFixed(2)}</span>
                      </div>
                    )}
                  </div>
                )}

                <div className="flex space-x-2">
                  <Button type="submit" disabled={formData.producto_id === 0}>
                    Registrar Venta
                  </Button>
                  <Button type="button" variant="outline" onClick={resetForm}>
                    Cancelar
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Historial de Ventas</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-4 font-medium">Fecha</th>
                    <th className="text-left p-4 font-medium">Producto</th>
                    {usuario?.rol === 'admin' && (
                      <th className="text-left p-4 font-medium">Vendedor</th>
                    )}
                    <th className="text-right p-4 font-medium">Cantidad</th>
                    <th className="text-right p-4 font-medium">Precio Unit.</th>
                    <th className="text-right p-4 font-medium">Total</th>
                    <th className="text-right p-4 font-medium">Comisión</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {ventas.map((venta) => (
                    <tr key={venta.id} className="hover:bg-gray-50">
                      <td className="p-4">
                        {new Date(venta.fecha_venta).toLocaleDateString('es-ES', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </td>
                      <td className="p-4">{venta.producto_nombre}</td>
                      {usuario?.rol === 'admin' && (
                        <td className="p-4">{venta.vendedor_nombre}</td>
                      )}
                      <td className="text-right p-4">{venta.cantidad}</td>
                      <td className="text-right p-4">${venta.precio_unitario.toFixed(2)}</td>
                      <td className="text-right p-4 font-medium">
                        ${venta.precio_total.toFixed(2)}
                      </td>
                      <td className="text-right p-4 text-green-600 font-medium">
                        ${venta.comision.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {ventas.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  No hay ventas registradas
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

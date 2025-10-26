import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { productosAPI } from '../services/api';
import type { Producto, ProductoCreate } from '../types';
import { Plus, Edit, Trash2, AlertCircle } from 'lucide-react';

export default function Productos() {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<ProductoCreate>({
    codigo_producto: '',
    nombre: '',
    descripcion: '',
    precio_venta: 0,
    precio_compra: 0,
    stock_actual: 0,
    stock_minimo: 0,
  });

  useEffect(() => {
    cargarProductos();
  }, []);

  const cargarProductos = async () => {
    try {
      const data = await productosAPI.getAll();
      setProductos(data);
    } catch (error) {
      console.error('Error al cargar productos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await productosAPI.update(editingId, formData);
      } else {
        await productosAPI.create(formData);
      }
      resetForm();
      cargarProductos();
    } catch (error) {
      console.error('Error al guardar producto:', error);
    }
  };

  const handleEdit = (producto: Producto) => {
    setEditingId(producto.id);
    setFormData({
      codigo_producto: producto.codigo_producto,
      nombre: producto.nombre,
      descripcion: producto.descripcion || '',
      precio_venta: producto.precio_venta,
      precio_compra: producto.precio_compra,
      stock_actual: producto.stock_actual,
      stock_minimo: producto.stock_minimo,
    });
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de eliminar este producto?')) {
      try {
        await productosAPI.delete(id);
        cargarProductos();
      } catch (error) {
        console.error('Error al eliminar producto:', error);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      codigo_producto: '',
      nombre: '',
      descripcion: '',
      precio_venta: 0,
      precio_compra: 0,
      stock_actual: 0,
      stock_minimo: 0,
    });
    setEditingId(null);
    setShowForm(false);
  };

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
          <h2 className="text-2xl font-bold text-gray-900">Gestión de Productos</h2>
          <Button onClick={() => setShowForm(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Nuevo Producto
          </Button>
        </div>

        {showForm && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>{editingId ? 'Editar Producto' : 'Nuevo Producto'}</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Código</label>
                    <Input
                      value={formData.codigo_producto}
                      onChange={(e) =>
                        setFormData({ ...formData, codigo_producto: e.target.value })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Nombre</label>
                    <Input
                      value={formData.nombre}
                      onChange={(e) =>
                        setFormData({ ...formData, nombre: e.target.value })
                      }
                      required
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium mb-1">Descripción</label>
                    <Input
                      value={formData.descripcion}
                      onChange={(e) =>
                        setFormData({ ...formData, descripcion: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Precio Compra</label>
                    <Input
                      type="number"
                      step="0.01"
                      value={formData.precio_compra}
                      onChange={(e) =>
                        setFormData({ ...formData, precio_compra: parseFloat(e.target.value) })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Precio Venta</label>
                    <Input
                      type="number"
                      step="0.01"
                      value={formData.precio_venta}
                      onChange={(e) =>
                        setFormData({ ...formData, precio_venta: parseFloat(e.target.value) })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Stock Actual</label>
                    <Input
                      type="number"
                      value={formData.stock_actual}
                      onChange={(e) =>
                        setFormData({ ...formData, stock_actual: parseInt(e.target.value) })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Stock Mínimo</label>
                    <Input
                      type="number"
                      value={formData.stock_minimo}
                      onChange={(e) =>
                        setFormData({ ...formData, stock_minimo: parseInt(e.target.value) })
                      }
                      required
                    />
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button type="submit">
                    {editingId ? 'Actualizar' : 'Crear'}
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
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-4 font-medium">Código</th>
                    <th className="text-left p-4 font-medium">Nombre</th>
                    <th className="text-right p-4 font-medium">Precio Venta</th>
                    <th className="text-right p-4 font-medium">Stock</th>
                    <th className="text-center p-4 font-medium">Estado</th>
                    <th className="text-right p-4 font-medium">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {productos.map((producto) => (
                    <tr key={producto.id} className="hover:bg-gray-50">
                      <td className="p-4">{producto.codigo_producto}</td>
                      <td className="p-4">
                        <div>
                          <div className="font-medium">{producto.nombre}</div>
                          {producto.descripcion && (
                            <div className="text-sm text-gray-500">{producto.descripcion}</div>
                          )}
                        </div>
                      </td>
                      <td className="text-right p-4">${producto.precio_venta.toFixed(2)}</td>
                      <td className="text-right p-4">
                        <div className="flex items-center justify-end">
                          {producto.stock_actual}
                          {producto.stock_actual <= producto.stock_minimo && (
                            <AlertCircle className="w-4 h-4 ml-2 text-red-500" />
                          )}
                        </div>
                      </td>
                      <td className="text-center p-4">
                        <span
                          className={`px-2 py-1 rounded-full text-xs ${
                            producto.activo
                              ? 'bg-green-100 text-green-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {producto.activo ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>
                      <td className="text-right p-4">
                        <div className="flex justify-end space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleEdit(producto)}
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="destructive"
                            onClick={() => handleDelete(producto.id)}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

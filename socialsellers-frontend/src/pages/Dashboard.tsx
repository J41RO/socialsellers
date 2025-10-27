import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import Button from '../components/ui/Button';
import { reportesAPI, ventasAPI, notificacionesAPI } from '../services/api';
import type { MetricasGenerales, Venta, NotificacionTest } from '../types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { DollarSign, TrendingUp, Package, AlertTriangle, Bell } from 'lucide-react';

export default function Dashboard() {
  const { usuario } = useAuth();
  const [metricas, setMetricas] = useState<MetricasGenerales | null>(null);
  const [ventasRecientes, setVentasRecientes] = useState<Venta[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [testResult, setTestResult] = useState<NotificacionTest | null>(null);
  const [testLoading, setTestLoading] = useState(false);

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        if (usuario?.rol === 'admin') {
          const metricasData = await reportesAPI.getMetricas();
          setMetricas(metricasData);
        }

        const ventasData = usuario?.rol === 'admin'
          ? await ventasAPI.getAll()
          : await ventasAPI.getByVendedor(usuario?.id || 0);

        setVentasRecientes(ventasData.slice(-10));
      } catch (error) {
        console.error('Error al cargar datos:', error);
      } finally {
        setIsLoading(false);
      }
    };

    cargarDatos();
  }, [usuario]);

  const ventasPorDia = ventasRecientes.reduce((acc: any, venta) => {
    const fecha = new Date(venta.fecha_venta).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
    const existing = acc.find((item: any) => item.fecha === fecha);
    if (existing) {
      existing.total += venta.precio_total;
      existing.cantidad += 1;
    } else {
      acc.push({ fecha, total: venta.precio_total, cantidad: 1 });
    }
    return acc;
  }, []);

  const handleTestNotificaciones = async () => {
    setTestLoading(true);
    setTestResult(null);
    try {
      const result = await notificacionesAPI.test();
      setTestResult(result);
    } catch (error) {
      console.error('Error al probar notificaciones:', error);
      setTestResult({
        email_sent: false,
        whatsapp_sent: false,
        mensaje: 'Error al enviar notificaciones de prueba',
      });
    } finally {
      setTestLoading(false);
    }
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
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Bienvenido, {usuario?.nombre}
        </h2>

        {/* Métricas principales (solo admin) */}
        {usuario?.rol === 'admin' && metricas && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Ventas Totales</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">${metricas.total_ventas.toFixed(2)}</div>
                <p className="text-xs text-muted-foreground">
                  ${metricas.ventas_mes_actual.toFixed(2)} este mes
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Comisiones</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">${metricas.total_comisiones.toFixed(2)}</div>
                <p className="text-xs text-muted-foreground">
                  ${metricas.comisiones_mes_actual.toFixed(2)} este mes
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Productos</CardTitle>
                <Package className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metricas.total_productos}</div>
                <p className="text-xs text-muted-foreground">Total en catálogo</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Stock Bajo</CardTitle>
                <AlertTriangle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metricas.productos_bajo_stock}</div>
                <p className="text-xs text-muted-foreground">Requieren atención</p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Gráfico de ventas */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <Card>
            <CardHeader>
              <CardTitle>Ventas por Día</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={ventasPorDia}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="fecha" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="total" stroke="#2563eb" name="Total ($)" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Cantidad de Ventas</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={ventasPorDia}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="fecha" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="cantidad" fill="#10b981" name="Ventas" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Centro de Notificaciones */}
        {usuario?.rol === 'admin' && (
          <Card className="mb-6">
            <CardHeader className="flex flex-row items-center justify-between">
              <div className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-blue-600" />
                <CardTitle>Centro de Notificaciones</CardTitle>
              </div>
              <Button
                onClick={handleTestNotificaciones}
                disabled={testLoading}
                variant="outline"
                size="sm"
              >
                {testLoading ? 'Enviando...' : 'Probar Notificaciones'}
              </Button>
            </CardHeader>
            <CardContent>
              {testResult && (
                <div className={`p-4 rounded-md ${
                  testResult.email_sent && testResult.whatsapp_sent
                    ? 'bg-green-50 border border-green-200'
                    : 'bg-yellow-50 border border-yellow-200'
                }`}>
                  <p className="font-medium mb-2">{testResult.mensaje}</p>
                  <div className="text-sm space-y-1">
                    <div className="flex items-center gap-2">
                      <span className={testResult.email_sent ? 'text-green-600' : 'text-red-600'}>
                        {testResult.email_sent ? '✓' : '✗'}
                      </span>
                      <span>Email {testResult.email_sent ? 'enviado' : 'no enviado'}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={testResult.whatsapp_sent ? 'text-green-600' : 'text-red-600'}>
                        {testResult.whatsapp_sent ? '✓' : '✗'}
                      </span>
                      <span>WhatsApp {testResult.whatsapp_sent ? 'enviado' : 'no enviado'}</span>
                    </div>
                  </div>
                </div>
              )}
              {!testResult && (
                <p className="text-sm text-gray-600">
                  Sistema de notificaciones automáticas activo.
                  Haz clic en "Probar Notificaciones" para verificar el envío de alertas.
                </p>
              )}
            </CardContent>
          </Card>
        )}

        {/* Ventas recientes */}
        <Card>
          <CardHeader>
            <CardTitle>Ventas Recientes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Fecha</th>
                    <th className="text-left p-2">Producto</th>
                    <th className="text-right p-2">Cantidad</th>
                    <th className="text-right p-2">Total</th>
                    {usuario?.rol === 'admin' && <th className="text-left p-2">Vendedor</th>}
                  </tr>
                </thead>
                <tbody>
                  {ventasRecientes.map((venta) => (
                    <tr key={venta.id} className="border-b">
                      <td className="p-2">
                        {new Date(venta.fecha_venta).toLocaleDateString('es-ES')}
                      </td>
                      <td className="p-2">{venta.producto_nombre}</td>
                      <td className="text-right p-2">{venta.cantidad}</td>
                      <td className="text-right p-2">${venta.precio_total.toFixed(2)}</td>
                      {usuario?.rol === 'admin' && (
                        <td className="p-2">{venta.vendedor_nombre}</td>
                      )}
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

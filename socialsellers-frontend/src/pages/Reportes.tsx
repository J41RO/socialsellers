import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import Button from '../components/ui/Button';
import { reportesAPI } from '../services/api';
import type { RankingVendedor } from '../types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Download, Trophy } from 'lucide-react';

export default function Reportes() {
  const [ranking, setRanking] = useState<RankingVendedor[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    cargarRanking();
  }, []);

  const cargarRanking = async () => {
    try {
      const data = await reportesAPI.getRanking();
      setRanking(data);
    } catch (error) {
      console.error('Error al cargar ranking:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportar = async (formato: 'csv' | 'pdf') => {
    try {
      const blob = await reportesAPI.exportarVentas(formato);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ventas.${formato}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error al exportar:', error);
      alert('Error al exportar el reporte');
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
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Reportes y Rankings</h2>
          <div className="flex space-x-2">
            <Button variant="outline" onClick={() => handleExportar('csv')}>
              <Download className="w-4 h-4 mr-2" />
              Exportar CSV
            </Button>
            <Button variant="outline" onClick={() => handleExportar('pdf')}>
              <Download className="w-4 h-4 mr-2" />
              Exportar PDF
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Gráfico de ventas por vendedor */}
          <Card>
            <CardHeader>
              <CardTitle>Ventas Totales por Vendedor</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={ranking}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="vendedor_nombre" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="total_ventas" fill="#2563eb" name="Total Ventas ($)" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Gráfico de comisiones */}
          <Card>
            <CardHeader>
              <CardTitle>Comisiones por Vendedor</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={ranking}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="vendedor_nombre" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="total_comisiones" fill="#10b981" name="Comisiones ($)" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Tabla de ranking */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Trophy className="w-5 h-5 mr-2 text-yellow-500" />
              Ranking de Vendedores
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-center p-4 font-medium">Posición</th>
                    <th className="text-left p-4 font-medium">Vendedor</th>
                    <th className="text-right p-4 font-medium">Cantidad Ventas</th>
                    <th className="text-right p-4 font-medium">Total Ventas</th>
                    <th className="text-right p-4 font-medium">Total Comisiones</th>
                    <th className="text-right p-4 font-medium">Promedio por Venta</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {ranking.map((vendedor, index) => (
                    <tr
                      key={vendedor.vendedor_id}
                      className={`hover:bg-gray-50 ${
                        index === 0 ? 'bg-yellow-50' : ''
                      }`}
                    >
                      <td className="text-center p-4">
                        <div className="flex items-center justify-center">
                          {index === 0 && (
                            <Trophy className="w-5 h-5 text-yellow-500 mr-2" />
                          )}
                          <span className="font-bold text-lg">{index + 1}</span>
                        </div>
                      </td>
                      <td className="p-4 font-medium">{vendedor.vendedor_nombre}</td>
                      <td className="text-right p-4">{vendedor.cantidad_ventas}</td>
                      <td className="text-right p-4 font-medium">
                        ${vendedor.total_ventas.toFixed(2)}
                      </td>
                      <td className="text-right p-4 text-green-600 font-medium">
                        ${vendedor.total_comisiones.toFixed(2)}
                      </td>
                      <td className="text-right p-4">
                        ${(vendedor.total_ventas / vendedor.cantidad_ventas).toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot className="bg-gray-100 font-bold">
                  <tr>
                    <td colSpan={2} className="p-4 text-right">TOTAL:</td>
                    <td className="text-right p-4">
                      {ranking.reduce((sum, v) => sum + v.cantidad_ventas, 0)}
                    </td>
                    <td className="text-right p-4">
                      ${ranking.reduce((sum, v) => sum + v.total_ventas, 0).toFixed(2)}
                    </td>
                    <td className="text-right p-4 text-green-600">
                      ${ranking.reduce((sum, v) => sum + v.total_comisiones, 0).toFixed(2)}
                    </td>
                    <td></td>
                  </tr>
                </tfoot>
              </table>
              {ranking.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  No hay datos de ventas disponibles
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

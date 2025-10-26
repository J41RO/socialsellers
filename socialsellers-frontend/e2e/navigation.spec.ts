import { test, expect } from '@playwright/test';

test.describe('Navigation Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Simular sesión de admin
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.setItem('access_token', 'fake-admin-token');
      localStorage.setItem('usuario', JSON.stringify({
        id: 1,
        nombre: 'Admin Test',
        email: 'admin@test.com',
        rol: 'admin',
        activo: true
      }));
    });
  });

  test('should navigate between pages', async ({ page }) => {
    await page.goto('/dashboard');

    // Verificar dashboard
    await expect(page.locator('text=/dashboard/i')).toBeVisible();

    // Navegar a productos (solo admins)
    await page.click('text=/productos/i');
    await expect(page.url()).toContain('/productos');

    // Navegar a ventas
    await page.click('text=/ventas/i');
    await expect(page.url()).toContain('/ventas');

    // Navegar a reportes (solo admins)
    await page.click('text=/reportes/i');
    await expect(page.url()).toContain('/reportes');
  });

  test('should display user info in navbar', async ({ page }) => {
    await page.goto('/dashboard');

    // Verificar que el nombre del usuario y rol se muestran
    await expect(page.locator('text=Admin Test')).toBeVisible();
    await expect(page.locator('text=admin')).toBeVisible();
  });

  test('should logout successfully', async ({ page }) => {
    await page.goto('/dashboard');

    // Click en botón de logout
    await page.click('button:has-text("Salir")');

    // Debería redirigir a login y limpiar localStorage
    await expect(page.url()).toContain('/login');

    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeNull();
  });
});

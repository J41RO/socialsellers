import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';

describe('Card Components', () => {
  it('renders Card with content', () => {
    render(<Card>Card content</Card>);
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });

  it('renders CardHeader with CardTitle', () => {
    render(
      <CardHeader>
        <CardTitle>Test Title</CardTitle>
      </CardHeader>
    );
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('renders CardDescription', () => {
    render(<CardDescription>Test description</CardDescription>);
    expect(screen.getByText('Test description')).toBeInTheDocument();
  });

  it('renders complete Card structure', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Title</CardTitle>
          <CardDescription>Description</CardDescription>
        </CardHeader>
        <CardContent>Content</CardContent>
        <CardFooter>Footer</CardFooter>
      </Card>
    );
    expect(screen.getByText('Title')).toBeInTheDocument();
    expect(screen.getByText('Description')).toBeInTheDocument();
    expect(screen.getByText('Content')).toBeInTheDocument();
    expect(screen.getByText('Footer')).toBeInTheDocument();
  });
});

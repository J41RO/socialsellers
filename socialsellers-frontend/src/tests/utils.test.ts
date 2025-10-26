import { describe, it, expect } from 'vitest';
import { cn } from '../lib/utils';

describe('Utils - cn function', () => {
  it('merges class names', () => {
    const result = cn('class1', 'class2');
    expect(result).toContain('class1');
    expect(result).toContain('class2');
  });

  it('handles conditional classes', () => {
    const result = cn('base', true && 'conditional', false && 'ignored');
    expect(result).toContain('base');
    expect(result).toContain('conditional');
    expect(result).not.toContain('ignored');
  });

  it('handles undefined and null values', () => {
    const result = cn('class1', undefined, null, 'class2');
    expect(result).toContain('class1');
    expect(result).toContain('class2');
  });

  it('merges tailwind classes correctly', () => {
    const result = cn('px-2 py-1', 'px-4');
    // tailwind-merge should keep only px-4
    expect(result).toContain('px-4');
    expect(result).toContain('py-1');
  });
});

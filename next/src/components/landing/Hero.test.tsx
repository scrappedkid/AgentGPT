import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { describe, it, expect } from 'jest';
import Hero from './Hero';

describe('Hero', () => {
  it('renders correctly', () => {
    render(<Hero />);
    expect(screen.getByText('Web Extraction At Your Fingertips.')).toBeInTheDocument();
  });

  it('handles window resize event', () => {
    render(<Hero />);
    global.innerWidth = 500;
    fireEvent(window, new Event('resize'));
    expect(screen.getByAltText('A 3D blob that seems to represent most AI companies')).toBeInTheDocument();
  });

  it('handles click on left slider button', () => {
    render(<Hero />);
    fireEvent.click(screen.getByRole('button', { name: /left slider button/i }));
    expect(screen.getByText('Manufacturing')).toBeInTheDocument();
  });

  it('handles click on right slider button', () => {
    render(<Hero />);
    fireEvent.click(screen.getByRole('button', { name: /right slider button/i }));
    expect(screen.getByText('E-commerce')).toBeInTheDocument();
  });

  it('renders correctly with different props and state', () => {
    render(<Hero className="test-class" />);
    expect(screen.getByText('Web Extraction At Your Fingertips.')).toHaveClass('test-class');
  });
});

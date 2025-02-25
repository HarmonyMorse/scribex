/* global jest, describe, beforeEach, test, expect */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ApiTest from './ApiTest';
import { checkHealth } from '../services/api';

// Mock the API service
jest.mock('../services/api', () => ({
    checkHealth: jest.fn(),
}));

describe('ApiTest Component', () => {
    beforeEach(() => {
        jest.resetAllMocks();
    });

    test('renders the test button', () => {
        render(<ApiTest />);
        expect(screen.getByText('Test API Connection')).toBeInTheDocument();
    });

    test('shows loading state when button is clicked', async () => {
        // Mock the API response to delay
        checkHealth.mockImplementation(() => new Promise(resolve => setTimeout(() => {
            resolve({ status: 'healthy' });
        }, 100)));

        render(<ApiTest />);

        fireEvent.click(screen.getByText('Test API Connection'));

        expect(screen.getByText('Testing...')).toBeInTheDocument();

        await waitFor(() => {
            expect(screen.getByText('API Response:')).toBeInTheDocument();
        });
    });

    test('displays API response when successful', async () => {
        const mockResponse = {
            status: 'healthy',
            version: '0.1.0',
            database: 'connected',
            environment: 'development'
        };

        checkHealth.mockResolvedValue(mockResponse);

        render(<ApiTest />);

        fireEvent.click(screen.getByText('Test API Connection'));

        await waitFor(() => {
            expect(screen.getByText('API Response:')).toBeInTheDocument();
            expect(screen.getByText(/"status": "healthy"/)).toBeInTheDocument();
        });
    });

    test('displays error when API call fails', async () => {
        checkHealth.mockRejectedValue(new Error('Network Error'));

        render(<ApiTest />);

        fireEvent.click(screen.getByText('Test API Connection'));

        await waitFor(() => {
            expect(screen.getByText('Error:')).toBeInTheDocument();
            expect(screen.getByText('Network Error')).toBeInTheDocument();
        });
    });
}); 
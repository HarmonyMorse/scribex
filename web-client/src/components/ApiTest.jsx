import { useState } from 'react';
import { checkHealth } from '../services/api';
import { Button } from './ui/button';

export default function ApiTest() {
    const [apiResponse, setApiResponse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleTestApi = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await checkHealth();
            setApiResponse(response);
        } catch (err) {
            setError(err.message || 'Failed to connect to API');
            setApiResponse(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md">
            <h2 className="text-xl font-bold mb-4">API Connection Test</h2>

            <Button
                onClick={handleTestApi}
                disabled={loading}
                className="mb-4"
            >
                {loading ? 'Testing...' : 'Test API Connection'}
            </Button>

            {error && (
                <div className="p-3 bg-red-100 text-red-700 rounded mb-4">
                    <p className="font-bold">Error:</p>
                    <p>{error}</p>
                </div>
            )}

            {apiResponse && (
                <div className="p-3 bg-green-100 text-green-700 rounded">
                    <p className="font-bold">API Response:</p>
                    <pre className="mt-2 whitespace-pre-wrap">
                        {JSON.stringify(apiResponse, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
} 
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ApiTest from './components/ApiTest';
import './App.css';

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <div className="container mx-auto py-8">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold">ScribeX</h1>
          <p className="text-gray-600">AI-Powered Writing Education Platform</p>
        </header>
        <main>
          <ApiTest />
        </main>
      </div>
    ),
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;

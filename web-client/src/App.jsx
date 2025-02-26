import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { useScreenSize } from './hooks/useScreenSize';
import ScreenSizeWarning from './components/ScreenSizeWarning';
import ApiTest from './components/ApiTest';
import './App.css';

// Temporary mock for user type - replace with actual auth state later
const isStudent = true;

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
  const { isScreenTooLarge } = useScreenSize();

  // Show warning only for students on large screens
  if (isStudent && isScreenTooLarge) {
    return <ScreenSizeWarning />;
  }

  return <RouterProvider router={router} />;
}

export default App;

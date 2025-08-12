import { Outlet } from 'react-router-dom'
import { Navbar } from '../components/Navbar'

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <Navbar />
      <main>
        <Outlet />
      </main>
      <footer className="mt-16 border-t border-gray-200 dark:border-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 text-sm text-gray-500 dark:text-gray-400">
          <p>© {new Date().getFullYear()} React Tailwind Starter</p>
        </div>
      </footer>
    </div>
  )
}
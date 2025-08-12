import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="mx-auto max-w-xl px-4 sm:px-6 lg:px-8 py-16 text-center">
      <p className="text-sm font-semibold text-primary-600">404</p>
      <h2 className="mt-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Page not found</h2>
      <p className="mt-2 text-gray-600 dark:text-gray-300">Sorry, we couldn’t find the page you’re looking for.</p>
      <div className="mt-6">
        <Link to="/" className="text-sm font-semibold text-primary-600 hover:text-primary-500">
          Go back home
        </Link>
      </div>
    </div>
  )
}
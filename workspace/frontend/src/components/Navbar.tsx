import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { ThemeToggle } from './ThemeToggle'

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <header className="border-b border-gray-200 dark:border-gray-800 bg-white/70 dark:bg-gray-900/70 backdrop-blur supports-[backdrop-filter]:bg-white/60 sticky top-0 z-40">
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-14 items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-md bg-primary-600 text-white font-bold">R</span>
            <span className="text-sm font-semibold tracking-wide text-gray-900 dark:text-gray-100">React Tailwind</span>
          </div>

          <div className="hidden md:flex items-center gap-6">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `text-sm font-medium transition-colors ${isActive ? 'text-primary-600' : 'text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white'}`
              }
            >
              Home
            </NavLink>
            <NavLink
              to="/about"
              className={({ isActive }) =>
                `text-sm font-medium transition-colors ${isActive ? 'text-primary-600' : 'text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white'}`
              }
            >
              About
            </NavLink>
            <ThemeToggle />
          </div>

          <div className="md:hidden flex items-center gap-2">
            <ThemeToggle />
            <button
              aria-label="Toggle menu"
              onClick={() => setIsOpen((v) => !v)}
              className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
                {isOpen ? (
                  <path fillRule="evenodd" d="M5.47 5.47a.75.75 0 0 1 1.06 0L12 10.94l5.47-5.47a.75.75 0 1 1 1.06 1.06L13.06 12l5.47 5.47a.75.75 0 0 1-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 0 1-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 0 1 0-1.06Z" clipRule="evenodd" />
                ) : (
                  <path fillRule="evenodd" d="M3.75 5.25A.75.75 0 0 1 4.5 4.5h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Zm0 7.5a.75.75 0 0 1 .75-.75h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Zm0 6a.75.75 0 0 1 .75-.75h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {isOpen && (
          <div className="md:hidden py-2 border-t border-gray-200 dark:border-gray-800">
            <div className="flex flex-col gap-2 py-2">
              <NavLink
                to="/"
                end
                onClick={() => setIsOpen(false)}
                className={({ isActive }) =>
                  `px-2 py-1.5 rounded-md text-sm font-medium ${isActive ? 'text-primary-600 bg-primary-50 dark:bg-gray-800' : 'text-gray-700 hover:bg-gray-50 dark:text-gray-200 dark:hover:bg-gray-800'}`
                }
              >
                Home
              </NavLink>
              <NavLink
                to="/about"
                onClick={() => setIsOpen(false)}
                className={({ isActive }) =>
                  `px-2 py-1.5 rounded-md text-sm font-medium ${isActive ? 'text-primary-600 bg-primary-50 dark:bg-gray-800' : 'text-gray-700 hover:bg-gray-50 dark:text-gray-200 dark:hover:bg-gray-800'}`
                }
              >
                About
              </NavLink>
            </div>
          </div>
        )}
      </nav>
    </header>
  )
}
import { useEffect, useState } from 'react'

type Theme = 'light' | 'dark'

function getPreferredTheme(): Theme {
  if (typeof window === 'undefined') return 'light'
  const stored = window.localStorage.getItem('theme') as Theme | null
  if (stored === 'light' || stored === 'dark') return stored
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  return prefersDark ? 'dark' : 'light'
}

function applyTheme(theme: Theme) {
  const root = document.documentElement
  if (theme === 'dark') {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(() => getPreferredTheme())

  useEffect(() => {
    applyTheme(theme)
    window.localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <button
      type="button"
      aria-label="Toggle dark mode"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="inline-flex items-center gap-2 rounded-md border border-gray-200 dark:border-gray-800 px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800"
    >
      {theme === 'dark' ? (
        <>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
            <path d="M21.752 15.002A9.718 9.718 0 0 1 12 21.75c-5.385 0-9.75-4.365-9.75-9.75 0-4.118 2.574-7.63 6.18-9.026a.75.75 0 0 1 .976.97A7.501 7.501 0 0 0 12 19.5a7.5 7.5 0 0 0 7.35-6.02.75.75 0 0 1 1.402.522Z" />
          </svg>
          Dark
        </>
      ) : (
        <>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
            <path fillRule="evenodd" d="M12 2.25a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0V3A.75.75 0 0 1 12 2.25Zm0 15a3.75 3.75 0 1 0 0-7.5 3.75 3.75 0 0 0 0 7.5ZM4.5 12a.75.75 0 0 1-.75.75H2.25a.75.75 0 0 1 0-1.5H3.75A.75.75 0 0 1 4.5 12Zm18 0a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75ZM6.116 6.116a.75.75 0 0 1 1.06 0l1.06 1.06a.75.75 0 1 1-1.06 1.06l-1.06-1.06a.75.75 0 0 1 0-1.06Zm11.648 11.648a.75.75 0 0 1 1.06 0l1.06 1.06a.75.75 0 0 1-1.06 1.06l-1.06-1.06a.75.75 0 0 1 0-1.06ZM12 18.75a.75.75 0 0 1 .75.75V21a.75.75 0 0 1-1.5 0v-1.5a.75.75 0 0 1 .75-.75ZM18 12a.75.75 0 0 1 .75-.75h1.5a.75.75 0 0 1 0 1.5h-1.5A.75.75 0 0 1 18 12Zm-9.75 9a.75.75 0 0 1 .75-.75H10.5a.75.75 0 0 1 0 1.5H9a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
          </svg>
          Light
        </>
      )}
    </button>
  )
}
export default function Home() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      <section className="text-center">
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
          React + Tailwind + TypeScript
        </h1>
        <p className="mt-3 text-gray-600 dark:text-gray-300">
          Starter app with a responsive navbar, dark mode, and routing.
        </p>
        <div className="mt-6">
          <a
            href="https://tailwindcss.com/docs"
            target="_blank"
            className="inline-flex items-center rounded-md bg-primary-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            Read Tailwind Docs
          </a>
        </div>
      </section>

      <section className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, idx) => (
          <div key={idx} className="rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5">
            <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100">Card {idx + 1}</h3>
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">
              Example content block styled with Tailwind utilities.
            </p>
          </div>
        ))}
      </section>
    </div>
  )
}
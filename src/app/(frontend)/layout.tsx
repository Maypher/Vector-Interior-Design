import './globals.css'

export default async function RootLayout(props: { children: React.ReactNode }) {
  const { children } = props

  return (
    <html>
      <body>{children}</body>
    </html>
  )
}

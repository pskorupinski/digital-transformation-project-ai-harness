import type { ReactNode } from 'react'
import { BRAND } from '../brand'

type Props = {
  children: ReactNode
  /** Links for the header navigation, e.g. <li><a href="/trips">Trips</a></li> */
  nav?: ReactNode
  footer?: ReactNode
}

// Page frame: brand top left, optional navigation, content, footer. Styled by base.css.
export default function Layout({ children, nav, footer }: Props) {
  return (
    <>
      <header>
        <a href="/">
          {BRAND.logo && <img src={BRAND.logo} alt="" />}
          {BRAND.name}
        </a>
        {nav && (
          <nav aria-label="Main">
            <ul>{nav}</ul>
          </nav>
        )}
      </header>
      <main>{children}</main>
      <footer>{footer}</footer>
    </>
  )
}

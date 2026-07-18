import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Pill, Activity, FileText, Stethoscope } from 'lucide-react'
import { useState } from 'react'
import './Header.css'

const navLinks = [
    { path: '/drug-interaction', label: 'Drug Interactions', icon: Pill },
    { path: '/drug-details', label: 'Drug Details', icon: FileText },
    { path: '/symptom-checker', label: 'Symptom Checker', icon: Stethoscope },
]

function Header() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
    const location = useLocation()

    return (
        <header className="header">
            <div className="container">
                <div className="header__inner">
                    <Link to="/" className="header__logo">
                        <div className="header__logo-icon">
                            <Activity size={24} />
                        </div>
                        <span className="header__logo-text">
                            Med<span className="text-gradient">AI</span>
                        </span>
                    </Link>

                    <nav className={`header__nav ${mobileMenuOpen ? 'header__nav--open' : ''}`}>
                        {navLinks.map(({ path, label, icon: Icon }) => (
                            <Link
                                key={path}
                                to={path}
                                className={`header__nav-link ${location.pathname === path ? 'header__nav-link--active' : ''}`}
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                <Icon size={18} />
                                <span>{label}</span>
                            </Link>
                        ))}
                    </nav>

                    <button
                        className="header__mobile-toggle"
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        aria-label="Toggle menu"
                    >
                        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>
            </div>
        </header>
    )
}

export default Header

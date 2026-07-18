import { Github, Mail } from 'lucide-react'
import { Link } from 'react-router-dom'
import './Footer.css'

function Footer() {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer__inner">
                    <div className="footer__brand">
                        <Link to="/" className="footer__logo">
                            Med<span className="text-gradient">AI</span>
                        </Link>
                        <p className="footer__tagline">
                            AI-powered medical assistant for smarter health decisions.
                        </p>
                    </div>

                    <div className="footer__links">
                        <div className="footer__link-group">
                            <h4>Features</h4>
                            <Link to="/drug-interaction">Drug Interactions</Link>
                            <Link to="/drug-details">Drug Details</Link>
                            <Link to="/symptom-checker">Symptom Checker</Link>
                        </div>
                    </div>

                    <div className="footer__bottom">
                        <p className="footer__disclaimer">
                            ⚠️ This tool is for informational purposes only. Always consult a healthcare professional.
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer

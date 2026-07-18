import { Link } from 'react-router-dom'
import {
    Pill,
    FileText,
    Stethoscope,
    ArrowRight,
    Shield,
    Zap,
    Brain,
    CheckCircle,
    Activity
} from 'lucide-react'
import './Landing.css'

const features = [
    {
        icon: Pill,
        title: 'Drug Interaction Checker',
        description: 'Instantly check for drug-drug, drug-food interactions and therapeutic duplications with AI-powered analysis.',
        link: '/drug-interaction',
        color: 'blue'
    },
    {
        icon: FileText,
        title: 'Drug Details',
        description: 'Get comprehensive information about medications including uses, side effects, warnings, and more.',
        link: '/drug-details',
        color: 'purple'
    },
    {
        icon: Stethoscope,
        title: 'Symptom Checker',
        description: 'Describe your symptoms and receive AI-powered analysis of possible medical conditions.',
        link: '/symptom-checker',
        color: 'green'
    }
]

const benefits = [
    { icon: Zap, text: 'Instant AI Analysis' },
    { icon: Shield, text: 'Evidence-Based Results' },
    { icon: Brain, text: 'Powered by Advanced AI' },
    { icon: CheckCircle, text: 'Easy to Use' }
]

function Landing() {
    return (
        <div className="landing">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero__bg">
                    <div className="hero__orb hero__orb--1"></div>
                    <div className="hero__orb hero__orb--2"></div>
                    <div className="hero__orb hero__orb--3"></div>
                </div>

                <div className="container">
                    <div className="hero__content">
                        <div className="hero__badge animate-slide-down">
                            <Activity size={16} />
                            <span>AI-Powered Medical Assistant</span>
                        </div>

                        <h1 className="hero__title animate-slide-up">
                            Your Intelligent
                            <span className="text-gradient"> Health Companion</span>
                        </h1>

                        <p className="hero__subtitle animate-slide-up stagger-1">
                            Check drug interactions, explore medication details, and analyze symptoms
                            with cutting-edge AI technology. Make informed health decisions.
                        </p>

                        <div className="hero__actions animate-slide-up stagger-2">
                            <Link to="/drug-interaction" className="btn btn--primary btn--lg">
                                Get Started
                                <ArrowRight size={20} />
                            </Link>
                            <Link to="/symptom-checker" className="btn btn--secondary btn--lg">
                                Check Symptoms
                            </Link>
                        </div>

                        <div className="hero__benefits animate-slide-up stagger-3">
                            {benefits.map(({ icon: Icon, text }) => (
                                <div key={text} className="hero__benefit">
                                    <Icon size={18} />
                                    <span>{text}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features">
                <div className="container">
                    <div className="features__header">
                        <h2>Powerful Health Tools</h2>
                        <p>Everything you need to make informed decisions about your medications and health.</p>
                    </div>

                    <div className="features__grid">
                        {features.map(({ icon: Icon, title, description, link, color }, index) => (
                            <Link
                                to={link}
                                key={title}
                                className={`feature-card feature-card--${color} animate-slide-up stagger-${index + 1}`}
                            >
                                <div className="feature-card__icon">
                                    <Icon size={28} />
                                </div>
                                <h3 className="feature-card__title">{title}</h3>
                                <p className="feature-card__description">{description}</p>
                                <div className="feature-card__action">
                                    <span>Explore</span>
                                    <ArrowRight size={16} />
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="how-it-works">
                <div className="container">
                    <div className="how-it-works__header">
                        <h2>How It Works</h2>
                        <p>Get started in seconds with our simple three-step process.</p>
                    </div>

                    <div className="steps">
                        <div className="step animate-slide-up stagger-1">
                            <div className="step__number">1</div>
                            <h3>Enter Information</h3>
                            <p>Input your medications or describe your symptoms using our intuitive interface.</p>
                        </div>

                        <div className="step animate-slide-up stagger-2">
                            <div className="step__number">2</div>
                            <h3>AI Analysis</h3>
                            <p>Our advanced AI processes your information against medical knowledge bases.</p>
                        </div>

                        <div className="step animate-slide-up stagger-3">
                            <div className="step__number">3</div>
                            <h3>Get Results</h3>
                            <p>Receive detailed, actionable insights about interactions, risks, or conditions.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta">
                <div className="container">
                    <div className="cta__card glass-card glass-card--static">
                        <h2>Ready to Get Started?</h2>
                        <p>Start using MedAI today and take control of your health decisions.</p>
                        <div className="cta__actions">
                            <Link to="/drug-interaction" className="btn btn--primary btn--lg">
                                Check Drug Interactions
                                <ArrowRight size={20} />
                            </Link>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default Landing

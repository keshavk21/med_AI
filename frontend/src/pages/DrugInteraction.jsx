import { useState } from 'react'
import {
    Search,
    X,
    Plus,
    AlertTriangle,
    AlertCircle,
    CheckCircle,
    Pill,
    Apple,
    Copy,
    ChevronDown,
    ChevronUp
} from 'lucide-react'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { checkDrugInteractions } from '../services/api'
import './DrugInteraction.css'

function DrugInteraction() {
    const [drugInput, setDrugInput] = useState('')
    const [drugs, setDrugs] = useState([])
    const [results, setResults] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [expandedSections, setExpandedSections] = useState({})

    const handleAddDrug = () => {
        const trimmedDrug = drugInput.trim()
        if (trimmedDrug && !drugs.includes(trimmedDrug)) {
            setDrugs([...drugs, trimmedDrug])
            setDrugInput('')
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleAddDrug()
        }
    }

    const handleRemoveDrug = (drugToRemove) => {
        setDrugs(drugs.filter(drug => drug !== drugToRemove))
    }

    const handleClear = () => {
        setDrugs([])
        setResults(null)
        setError(null)
    }

    const handleCheckInteractions = async () => {
        if (drugs.length < 2) {
            setError('Please add at least 2 medications to check for interactions.')
            return
        }

        setLoading(true)
        setError(null)
        setResults(null)

        try {
            const response = await checkDrugInteractions(drugs.join(', '))
            setResults(response.drug_interaction)
        } catch (err) {
            setError('Failed to check interactions. Please ensure the backend is running.')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const toggleSection = (section) => {
        setExpandedSections(prev => ({
            ...prev,
            [section]: !prev[section]
        }))
    }

    const getSeverityBadge = (level) => {
        const config = {
            Major: { icon: AlertTriangle, class: 'badge--major', label: 'Major' },
            Moderate: { icon: AlertCircle, class: 'badge--moderate', label: 'Moderate' },
            Minor: { icon: CheckCircle, class: 'badge--minor', label: 'Minor' }
        }
        return config[level] || null
    }

    const renderInteractionSection = (title, data, icon) => {
        if (!data) return null

        const Icon = icon
        const interactions = Object.entries(data).filter(([key]) => key !== 'No Interaction')
        const noInteraction = data['No Interaction']

        if (interactions.length === 0 && noInteraction) {
            return (
                <div className="interaction-section animate-slide-up">
                    <div className="interaction-section__header">
                        <div className="interaction-section__title">
                            <Icon size={20} />
                            <h3>{title}</h3>
                        </div>
                    </div>
                    <div className="interaction-section__content">
                        <div className="no-interaction">
                            <CheckCircle size={20} />
                            <span>{noInteraction}</span>
                        </div>
                    </div>
                </div>
            )
        }

        return (
            <div className="interaction-section animate-slide-up">
                <div
                    className="interaction-section__header"
                    onClick={() => toggleSection(title)}
                >
                    <div className="interaction-section__title">
                        <Icon size={20} />
                        <h3>{title}</h3>
                        <span className="interaction-section__count">{interactions.length} found</span>
                    </div>
                    {expandedSections[title] ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </div>

                {(expandedSections[title] !== false) && (
                    <div className="interaction-section__content">
                        {interactions.map(([level, description]) => {
                            const badge = getSeverityBadge(level)
                            if (!badge) return null

                            const BadgeIcon = badge.icon
                            return (
                                <div key={level} className="interaction-item">
                                    <div className={`badge ${badge.class}`}>
                                        <BadgeIcon size={12} />
                                        <span>{badge.label}</span>
                                    </div>
                                    <p>{description}</p>
                                </div>
                            )
                        })}
                    </div>
                )}
            </div>
        )
    }

    return (
        <div className="drug-interaction-page">
            <div className="container">
                {/* Page Header */}
                <div className="page-header animate-slide-down">
                    <div className="page-header__icon">
                        <Pill size={32} />
                    </div>
                    <div>
                        <h1>Drug Interaction Checker</h1>
                        <p>Check for potential interactions between your medications</p>
                    </div>
                </div>

                {/* Input Section */}
                <div className="input-section glass-card glass-card--static animate-slide-up">
                    <div className="search-input-wrapper">
                        <Search className="search-icon" size={20} />
                        <input
                            type="text"
                            className="input input--lg"
                            placeholder="Enter medication name..."
                            value={drugInput}
                            onChange={(e) => setDrugInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                        />
                        <button
                            className="btn btn--primary add-btn"
                            onClick={handleAddDrug}
                            disabled={!drugInput.trim()}
                        >
                            <Plus size={20} />
                            Add
                        </button>
                    </div>

                    {/* Drug Chips */}
                    {drugs.length > 0 && (
                        <div className="drug-chips">
                            {drugs.map(drug => (
                                <div key={drug} className="chip">
                                    <Pill size={14} />
                                    <span>{drug}</span>
                                    <button
                                        className="chip__remove"
                                        onClick={() => handleRemoveDrug(drug)}
                                        aria-label={`Remove ${drug}`}
                                    >
                                        <X size={12} />
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Action Buttons */}
                    <div className="action-buttons">
                        <button
                            className="btn btn--primary btn--lg"
                            onClick={handleCheckInteractions}
                            disabled={drugs.length < 2 || loading}
                        >
                            {loading ? 'Analyzing...' : 'Check Interactions'}
                        </button>
                        <button
                            className="btn btn--secondary"
                            onClick={handleClear}
                            disabled={drugs.length === 0}
                        >
                            Clear All
                        </button>
                    </div>

                    {drugs.length < 2 && drugs.length > 0 && (
                        <p className="helper-text">Add at least one more medication to check interactions</p>
                    )}
                </div>

                {/* Error Message */}
                {error && (
                    <div className="error-message animate-slide-up">
                        <AlertTriangle size={20} />
                        <span>{error}</span>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <LoadingSpinner message="Analyzing drug interactions with AI..." />
                )}

                {/* Results Section */}
                {results && !loading && (
                    <div className="results-section">
                        <h2 className="results-title">Interaction Results</h2>

                        {renderInteractionSection(
                            'Drug-Drug Interactions',
                            results.drug_drug_check,
                            Pill
                        )}

                        {renderInteractionSection(
                            'Drug-Food Interactions',
                            results.drug_food_check,
                            Apple
                        )}

                        {renderInteractionSection(
                            'Therapeutic Duplications',
                            results.therapeutic_check,
                            Copy
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}

export default DrugInteraction

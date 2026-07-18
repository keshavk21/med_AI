import { useState } from 'react'
import {
    Search,
    FileText,
    AlertTriangle,
    Pill,
    Activity,
    AlertCircle,
    Info,
    ChevronDown,
    ChevronUp
} from 'lucide-react'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { getDrugDetails } from '../services/api'
import './DrugDetails.css'

function DrugDetails() {
    const [drugName, setDrugName] = useState('')
    const [drugInfo, setDrugInfo] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [expandedCards, setExpandedCards] = useState({})

    const handleSearch = async () => {
        if (!drugName.trim()) return

        setLoading(true)
        setError(null)
        setDrugInfo(null)

        try {
            const response = await getDrugDetails(drugName.trim())
            setDrugInfo(response.drug_details)
            // Expand all cards by default
            setExpandedCards({
                description: true,
                use: true,
                sideEffects: true,
                warnings: true,
                interactions: true,
                overdose: true
            })
        } catch (err) {
            setError('Failed to fetch drug details. Please ensure the backend is running.')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch()
        }
    }

    const toggleCard = (cardId) => {
        setExpandedCards(prev => ({
            ...prev,
            [cardId]: !prev[cardId]
        }))
    }

    const InfoCard = ({ id, icon: Icon, title, content, variant = 'default' }) => {
        if (!content) return null

        const isExpanded = expandedCards[id] !== false

        return (
            <div className={`info-card info-card--${variant} animate-slide-up`}>
                <div
                    className="info-card__header"
                    onClick={() => toggleCard(id)}
                >
                    <div className="info-card__title">
                        <div className={`info-card__icon info-card__icon--${variant}`}>
                            <Icon size={18} />
                        </div>
                        <h3>{title}</h3>
                    </div>
                    {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </div>
                {isExpanded && (
                    <div className="info-card__content">
                        <p>{content}</p>
                    </div>
                )}
            </div>
        )
    }

    return (
        <div className="drug-details-page">
            <div className="container">
                {/* Page Header */}
                <div className="page-header animate-slide-down">
                    <div className="page-header__icon">
                        <FileText size={32} />
                    </div>
                    <div>
                        <h1>Drug Details</h1>
                        <p>Get comprehensive information about any medication</p>
                    </div>
                </div>

                {/* Search Section */}
                <div className="search-section glass-card glass-card--static animate-slide-up">
                    <div className="search-input-wrapper">
                        <Search className="search-icon" size={20} />
                        <input
                            type="text"
                            className="input input--lg"
                            placeholder="Enter drug name (e.g., Aspirin, Metformin, Lisinopril)..."
                            value={drugName}
                            onChange={(e) => setDrugName(e.target.value)}
                            onKeyPress={handleKeyPress}
                        />
                        <button
                            className="btn btn--primary"
                            onClick={handleSearch}
                            disabled={!drugName.trim() || loading}
                        >
                            {loading ? 'Searching...' : 'Search'}
                        </button>
                    </div>

                    <div className="search-suggestions">
                        <span>Popular searches:</span>
                        {['Aspirin', 'Metformin', 'Lisinopril', 'Omeprazole'].map(drug => (
                            <button
                                key={drug}
                                className="suggestion-chip"
                                onClick={() => {
                                    setDrugName(drug)
                                    setTimeout(() => handleSearch(), 0)
                                }}
                            >
                                {drug}
                            </button>
                        ))}
                    </div>
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
                    <LoadingSpinner message="Fetching drug information with AI..." />
                )}

                {/* Drug Information */}
                {drugInfo && !loading && (
                    <div className="drug-info-section">
                        {/* Drug Title */}
                        <div className="drug-title-card glass-card animate-slide-up">
                            <div className="drug-title-header">
                                <div className="drug-title-icon">
                                    <Pill size={28} />
                                </div>
                                <div>
                                    <h2>{drugInfo.drug_title || drugName}</h2>
                                    <p className="drug-subtitle">Medication Information</p>
                                </div>
                            </div>
                        </div>

                        {/* Info Cards Grid */}
                        <div className="info-cards-grid">
                            <InfoCard
                                id="description"
                                icon={Info}
                                title="Description"
                                content={drugInfo.drug_description}
                                variant="default"
                            />

                            <InfoCard
                                id="use"
                                icon={Activity}
                                title={drugInfo.drug_use || "Medical Uses"}
                                content={drugInfo.drug_use_description}
                                variant="success"
                            />

                            <InfoCard
                                id="sideEffects"
                                icon={AlertCircle}
                                title={drugInfo.drug_side_effects || "Side Effects"}
                                content={drugInfo.drug_side_effects_description}
                                variant="warning"
                            />

                            <InfoCard
                                id="warnings"
                                icon={AlertTriangle}
                                title={drugInfo.drug_warnings || "Warnings"}
                                content={drugInfo.drug_warnings_description}
                                variant="danger"
                            />

                            <InfoCard
                                id="interactions"
                                icon={Pill}
                                title={drugInfo.drug_interactions || "Drug Interactions"}
                                content={drugInfo.drug_interactions_description}
                                variant="primary"
                            />

                            <InfoCard
                                id="overdose"
                                icon={AlertTriangle}
                                title={drugInfo.drug_overdose || "Overdose Information"}
                                content={drugInfo.drug_overdose_description}
                                variant="danger"
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default DrugDetails

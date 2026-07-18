import { useState } from 'react'
import {
    Stethoscope,
    X,
    Plus,
    AlertTriangle,
    User,
    Calendar,
    MapPin,
    ChevronRight,
    ChevronLeft,
    Activity,
    CheckCircle
} from 'lucide-react'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { checkSymptoms } from '../services/api'
import './SymptomChecker.css'

const countries = [
    'United States', 'India', 'United Kingdom', 'Canada', 'Australia',
    'Germany', 'France', 'Brazil', 'Japan', 'China', 'Mexico', 'Other'
]

const commonSymptoms = [
    'Headache', 'Fever', 'Cough', 'Fatigue', 'Nausea',
    'Dizziness', 'Chest Pain', 'Shortness of Breath', 'Back Pain', 'Sore Throat'
]

function SymptomChecker() {
    const [step, setStep] = useState(1)
    const [symptomInput, setSymptomInput] = useState('')
    const [symptoms, setSymptoms] = useState([])
    const [gender, setGender] = useState('')
    const [age, setAge] = useState('')
    const [country, setCountry] = useState('')
    const [results, setResults] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleAddSymptom = () => {
        const trimmedSymptom = symptomInput.trim()
        if (trimmedSymptom && !symptoms.includes(trimmedSymptom)) {
            setSymptoms([...symptoms, trimmedSymptom])
            setSymptomInput('')
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleAddSymptom()
        }
    }

    const handleRemoveSymptom = (symptomToRemove) => {
        setSymptoms(symptoms.filter(s => s !== symptomToRemove))
    }

    const handleAddCommonSymptom = (symptom) => {
        if (!symptoms.includes(symptom)) {
            setSymptoms([...symptoms, symptom])
        }
    }

    const canProceed = () => {
        switch (step) {
            case 1: return symptoms.length > 0
            case 2: return gender !== ''
            case 3: return age !== '' && parseInt(age) > 0 && parseInt(age) < 150
            case 4: return country !== ''
            default: return false
        }
    }

    const handleNext = () => {
        if (canProceed() && step < 4) {
            setStep(step + 1)
        }
    }

    const handleBack = () => {
        if (step > 1) {
            setStep(step - 1)
        }
    }

    const handleSubmit = async () => {
        if (!canProceed()) return

        setLoading(true)
        setError(null)
        setResults(null)

        try {
            const response = await checkSymptoms(symptoms, gender, parseInt(age), country)
            setResults(response.symptom_check)
            setStep(5) // Results step
        } catch (err) {
            setError('Failed to analyze symptoms. Please ensure the backend is running.')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleStartOver = () => {
        setStep(1)
        setSymptoms([])
        setGender('')
        setAge('')
        setCountry('')
        setResults(null)
        setError(null)
    }

    const renderStepIndicator = () => (
        <div className="step-indicator">
            {[1, 2, 3, 4].map(stepNum => (
                <div
                    key={stepNum}
                    className={`step-dot ${step >= stepNum ? 'step-dot--active' : ''} ${step === stepNum ? 'step-dot--current' : ''}`}
                >
                    {step > stepNum ? <CheckCircle size={16} /> : stepNum}
                </div>
            ))}
        </div>
    )

    const renderStep = () => {
        switch (step) {
            case 1:
                return (
                    <div className="step-content animate-slide-up">
                        <div className="step-header">
                            <Activity size={24} />
                            <h2>What symptoms are you experiencing?</h2>
                            <p>Add all relevant symptoms you're currently facing</p>
                        </div>

                        <div className="symptom-input-group">
                            <input
                                type="text"
                                className="input input--lg"
                                placeholder="Type a symptom..."
                                value={symptomInput}
                                onChange={(e) => setSymptomInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                            />
                            <button
                                className="btn btn--primary"
                                onClick={handleAddSymptom}
                                disabled={!symptomInput.trim()}
                            >
                                <Plus size={20} />
                                Add
                            </button>
                        </div>

                        <div className="common-symptoms">
                            <span className="common-symptoms__label">Quick add:</span>
                            <div className="common-symptoms__list">
                                {commonSymptoms.map(symptom => (
                                    <button
                                        key={symptom}
                                        className={`symptom-quick-add ${symptoms.includes(symptom) ? 'symptom-quick-add--added' : ''}`}
                                        onClick={() => handleAddCommonSymptom(symptom)}
                                        disabled={symptoms.includes(symptom)}
                                    >
                                        {symptom}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {symptoms.length > 0 && (
                            <div className="selected-symptoms">
                                <h4>Selected symptoms ({symptoms.length}):</h4>
                                <div className="symptoms-chips">
                                    {symptoms.map(symptom => (
                                        <div key={symptom} className="chip">
                                            <span>{symptom}</span>
                                            <button
                                                className="chip__remove"
                                                onClick={() => handleRemoveSymptom(symptom)}
                                            >
                                                <X size={12} />
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )

            case 2:
                return (
                    <div className="step-content animate-slide-up">
                        <div className="step-header">
                            <User size={24} />
                            <h2>What is your gender?</h2>
                            <p>This helps provide more accurate analysis</p>
                        </div>

                        <div className="gender-options">
                            {['Male', 'Female', 'Other'].map(g => (
                                <button
                                    key={g}
                                    className={`gender-option ${gender === g ? 'gender-option--selected' : ''}`}
                                    onClick={() => setGender(g)}
                                >
                                    <User size={24} />
                                    <span>{g}</span>
                                </button>
                            ))}
                        </div>
                    </div>
                )

            case 3:
                return (
                    <div className="step-content animate-slide-up">
                        <div className="step-header">
                            <Calendar size={24} />
                            <h2>What is your age?</h2>
                            <p>Age is an important factor in medical analysis</p>
                        </div>

                        <div className="age-input-wrapper">
                            <input
                                type="number"
                                className="input input--lg age-input"
                                placeholder="Enter your age"
                                value={age}
                                onChange={(e) => setAge(e.target.value)}
                                min="1"
                                max="150"
                            />
                            <span className="age-suffix">years old</span>
                        </div>
                    </div>
                )

            case 4:
                return (
                    <div className="step-content animate-slide-up">
                        <div className="step-header">
                            <MapPin size={24} />
                            <h2>Select your country</h2>
                            <p>Regional factors can affect health conditions</p>
                        </div>

                        <div className="country-grid">
                            {countries.map(c => (
                                <button
                                    key={c}
                                    className={`country-option ${country === c ? 'country-option--selected' : ''}`}
                                    onClick={() => setCountry(c)}
                                >
                                    {c}
                                </button>
                            ))}
                        </div>
                    </div>
                )

            case 5:
                return (
                    <div className="step-content animate-slide-up">
                        <div className="step-header">
                            <Stethoscope size={24} />
                            <h2>Analysis Results</h2>
                            <p>Based on your symptoms, here are possible conditions</p>
                        </div>

                        <div className="results-summary">
                            <div className="results-summary__item">
                                <span>Symptoms:</span>
                                <strong>{symptoms.join(', ')}</strong>
                            </div>
                            <div className="results-summary__item">
                                <span>Profile:</span>
                                <strong>{gender}, {age} years old, {country}</strong>
                            </div>
                        </div>

                        {results && (
                            <div className="conditions-list">
                                <h3>Possible Conditions</h3>
                                {Object.entries(results).map(([key, condition], index) => (
                                    <div
                                        key={key}
                                        className="condition-item"
                                        style={{ animationDelay: `${index * 0.1}s` }}
                                    >
                                        <div className="condition-rank">{index + 1}</div>
                                        <div className="condition-name">{condition}</div>
                                    </div>
                                ))}
                            </div>
                        )}

                        <div className="disclaimer-box">
                            <AlertTriangle size={20} />
                            <p>
                                <strong>Disclaimer:</strong> This is for informational purposes only and is not a substitute
                                for professional medical advice. Please consult a healthcare provider for proper diagnosis.
                            </p>
                        </div>

                        <button className="btn btn--secondary w-full" onClick={handleStartOver}>
                            Start New Analysis
                        </button>
                    </div>
                )

            default:
                return null
        }
    }

    return (
        <div className="symptom-checker-page">
            <div className="container">
                {/* Page Header */}
                <div className="page-header animate-slide-down">
                    <div className="page-header__icon">
                        <Stethoscope size={32} />
                    </div>
                    <div>
                        <h1>Symptom Checker</h1>
                        <p>AI-powered symptom analysis to help identify possible conditions</p>
                    </div>
                </div>

                {/* Main Card */}
                <div className="symptom-card glass-card glass-card--static">
                    {step < 5 && renderStepIndicator()}

                    {error && (
                        <div className="error-message">
                            <AlertTriangle size={20} />
                            <span>{error}</span>
                        </div>
                    )}

                    {loading ? (
                        <LoadingSpinner message="Analyzing your symptoms with AI..." />
                    ) : (
                        renderStep()
                    )}

                    {/* Navigation Buttons */}
                    {step < 5 && !loading && (
                        <div className="step-navigation">
                            <button
                                className="btn btn--secondary"
                                onClick={handleBack}
                                disabled={step === 1}
                            >
                                <ChevronLeft size={20} />
                                Back
                            </button>

                            {step < 4 ? (
                                <button
                                    className="btn btn--primary"
                                    onClick={handleNext}
                                    disabled={!canProceed()}
                                >
                                    Next
                                    <ChevronRight size={20} />
                                </button>
                            ) : (
                                <button
                                    className="btn btn--primary"
                                    onClick={handleSubmit}
                                    disabled={!canProceed()}
                                >
                                    Analyze Symptoms
                                    <Stethoscope size={20} />
                                </button>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default SymptomChecker

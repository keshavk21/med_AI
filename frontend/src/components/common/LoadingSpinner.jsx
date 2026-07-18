import './LoadingSpinner.css'

function LoadingSpinner({ size = 'md', message = 'Analyzing...' }) {
    return (
        <div className="loading-container">
            <div className={`loading-spinner loading-spinner--${size}`}>
                <div className="loading-spinner__ring"></div>
                <div className="loading-spinner__ring"></div>
                <div className="loading-spinner__ring"></div>
                <div className="loading-spinner__core"></div>
            </div>
            {message && <p className="loading-message">{message}</p>}
        </div>
    )
}

export default LoadingSpinner

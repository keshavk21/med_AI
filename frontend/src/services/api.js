const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const checkDrugInteractions = async (medications) => {
    const formData = new FormData()
    formData.append('selected_meds', medications)

    const response = await fetch(`${API_BASE_URL}/aggregate_interactions`, {
        method: 'POST',
        body: formData,
    })

    if (!response.ok) {
        throw new Error('Failed to check drug interactions')
    }

    return response.json()
}

export const getDrugDetails = async (drugName) => {
    const formData = new FormData()
    formData.append('selected_meds', drugName)

    const response = await fetch(`${API_BASE_URL}/drug_details`, {
        method: 'POST',
        body: formData,
    })

    if (!response.ok) {
        throw new Error('Failed to get drug details')
    }

    return response.json()
}

export const checkDrugDrug = async (medications) => {
    const formData = new FormData()
    formData.append('selected_meds', medications)

    const response = await fetch(`${API_BASE_URL}/drug_drug`, {
        method: 'POST',
        body: formData,
    })

    if (!response.ok) {
        throw new Error('Failed to check drug-drug interactions')
    }

    return response.json()
}

export const checkSymptoms = async (symptoms, gender, age, country) => {
    const response = await fetch(`${API_BASE_URL}/symptom_check`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            symptoms,
            gender,
            age: parseInt(age),
            country,
        }),
    })

    if (!response.ok) {
        throw new Error('Failed to check symptoms')
    }

    return response.json()
}

export const healthCheck = async () => {
    const response = await fetch(`${API_BASE_URL}/health`)

    if (!response.ok) {
        throw new Error('API is not healthy')
    }

    return response.json()
}

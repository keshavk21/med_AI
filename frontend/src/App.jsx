import { Routes, Route } from 'react-router-dom'
import Header from './components/Layout/Header'
import Footer from './components/Layout/Footer'
import Landing from './pages/Landing'
import DrugInteraction from './pages/DrugInteraction'
import DrugDetails from './pages/DrugDetails'
import SymptomChecker from './pages/SymptomChecker'

function App() {
    return (
        <div className="page-wrapper">
            <Header />
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<Landing />} />
                    <Route path="/drug-interaction" element={<DrugInteraction />} />
                    <Route path="/drug-details" element={<DrugDetails />} />
                    <Route path="/symptom-checker" element={<SymptomChecker />} />
                </Routes>
            </main>
            <Footer />
        </div>
    )
}

export default App

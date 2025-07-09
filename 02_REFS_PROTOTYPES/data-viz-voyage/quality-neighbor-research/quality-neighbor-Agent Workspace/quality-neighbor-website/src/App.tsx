import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import HomePage from './components/HomePage'
import MarketResearch from './components/MarketResearch'
import UserPersonas from './components/UserPersonas'
import BusinessStrategy from './components/BusinessStrategy'
import ProductDevelopment from './components/ProductDevelopment'
import BrandingDesign from './components/BrandingDesign'
import BusinessCase from './components/BusinessCase'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/market-research" element={<MarketResearch />} />
          <Route path="/user-personas" element={<UserPersonas />} />
          <Route path="/business-strategy" element={<BusinessStrategy />} />
          <Route path="/product-development" element={<ProductDevelopment />} />
          <Route path="/branding-design" element={<BrandingDesign />} />
          <Route path="/business-case" element={<BusinessCase />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

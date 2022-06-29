import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import HomeScreen from './screens/HomeScreen'
import Header from './components/Header'
import Footer from './components/Footer'
import AddSymbol from './components/AddSymbol'


function App() {
  return (
    <Router>
      <Header />
        <main>
          <Routes>
            <Route index element={<HomeScreen />} />
            <Route path="/add" element={<AddSymbol />} />
          </Routes>
        </main>
      
      <Footer />
    </Router>
  );
}

export default App;

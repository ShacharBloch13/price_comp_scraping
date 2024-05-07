import { useState } from 'react';
import axios from 'axios';
import styles from '../styles/Table.module.css';

export default function Home() {
  const [productName, setProductName] = useState('');
  const [recommendation, setRecommendation] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`http://127.0.0.1:8090/search`, {
        params: { product_name: productName }
      });
      console.log(response.data);
      setResults(response.data.data);  // Adjust based on the actual API response structure
      setRecommendation(response.data.recommendation);// might be an issue - check
    } catch (error) {
      console.error('Failed to fetch data:', error);
      setError('Failed to fetch data. Please try again.');
    }
    setLoading(false);
  };

  const constructURL = (result) => {
    if (result.Site === "Walmart") {
      return `https://www.walmart.com/search/?query=${encodeURIComponent(result['Item Title Name'])}`;
    } else if (result.Site === "Best Buy") {
      return `https://www.bestbuy.com/site/searchpage.jsp?st=${encodeURIComponent(result['Item Title Name'])}`;
    } else if (result.Site === "Newegg") {
      return `https://www.newegg.com/p/pl?d=${encodeURIComponent(result['Item Title Name'])}`;
    }
    return result['Go to website'] || '#'; // Fallback to provided URL or '#'
  };


  return (
    <div className={styles.tableContainer}>
      <h1 className={styles.h1}>Product Price Comparison</h1>
      <form onSubmit={handleSearch} className={styles.form}>
        <input
          className={styles.input}
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="Enter a product name"
          required
        />
        <button type="submit" disabled={loading} className={styles.button}>
          {loading ? 'Loading...' : 'Search'}
        </button>
      </form>
  
      {error && <p className={styles.text}>{error}</p>}
  
      <table className={styles.table}>
        <thead>
          <tr>
            <th className={styles.th}>Site</th>
            <th className={styles.th}>Product</th>
            <th className={styles.th}>Price</th>
            <th className={styles.th}>URL</th>
          </tr>
        </thead>
        <tbody>
          {results && results.length > 0 ? (
            results.map((result, index) => (
              <tr key={index}>
                 <td className={styles.td}>{result.Site}</td>
                    <td className={styles.td}>{result['Item Title Name']}</td>
                    <td className={styles.td}>{result['Price(USD)']}</td>
                    <td className={styles.td}>
                        <a href={constructURL(result)} target="_blank" rel="noopener noreferrer" className={styles.a}>
                            Go to product page 
                        </a>
                    </td>
         
              </tr>
            
            ))
          ) : (
            <tr>
              <td colSpan="4" className={styles.td}>No results found</td>
            </tr>
          )}
        </tbody>
      </table>
          {/* Recommendation display */}
          {recommendation && (
            <div className={styles.recommendationContainer}>
              <h2 className={styles.h2}>Recommended Product</h2>
              <p className={styles.text}>
                <a href={`https://www.google.com/search?q=${encodeURIComponent(recommendation)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.recommendationLink}>
                  {recommendation}
                </a>
              </p>
            </div>
          )}
    </div>
  );
}

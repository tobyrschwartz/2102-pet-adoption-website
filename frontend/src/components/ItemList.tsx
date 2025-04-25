import { useState, useEffect } from 'react';

// Define an interface for the item structure for type safety
interface Item {
  id: number;
  name: string;
  description: string;
}

function ItemList() {
  // Add types to state variables
  const [items, setItems] = useState<Item[]>([]); // Specify it's an array of Item objects
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null); // Error message is a string or null

  useEffect(() => {
    const fetchItems = async () => {
      try {
        setLoading(true); 
        setError(null); 

        const response = await fetch('http://localhost:5000/api/items', {
          credentials: 'include', // Ensures cookies are sent with the request
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          method: 'GET',
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Tell TypeScript to expect the data to match the Item interface array
        const data: Item[] = await response.json(); 
        console.log("Frontend: Fetched data:", data); 
        setItems(data); 

      } catch (err) {
        console.error("Frontend: Fetch error:", err);
        // Type guard to safely access err.message
        if (err instanceof Error) { 
          setError(err.message); 
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false); 
      }
    };

    fetchItems(); 

    return () => { }; // Cleanup function
  }, []); // Empty dependency array means run once on mount

  // --- Render logic (no changes needed here) ---
  if (loading) {
    return <div>Loading items...</div>;
  }

  if (error) {
    return <div>Error fetching items: {error}</div>;
  }

  return (
    <div>
      {/* <h2>Items from Backend</h2> */} {/* Moved heading to App.tsx */}
      {items.length > 0 ? (
        <ul>
          {items.map(item => (
            // Properties 'id', 'name', 'description' are now type-checked
            <li key={item.id}> 
              <strong>{item.name}:</strong> {item.description}
            </li>
          ))}
        </ul>
      ) : (
        <p>No items found.</p>
      )}
    </div>
  );
}

export default ItemList;
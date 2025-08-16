import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

function App() {
  const [pokemons, setPokemons] = useState([]);
  const [showForm, setShowForm] = useState(false);

  const [selectedPokemon, setSelectedPokemon] = useState(null);
  const [previewPokemon, setPreviewPokemon] = useState(null);
  const [releaseConfirm, setReleaseConfirm] = useState(null);
  const [nameEdit, setNameEdit] = useState(null);
  const [newName, setNewName] = useState('');
  const [formData, setFormData] = useState({
    pokedexNumber: ''
  });

  useEffect(() => {
    fetchPokemons();
  }, []);

  const fetchPokemons = async () => {
    try {
      const response = await axios.get(`${API_URL}/pokemons`);
      setPokemons(response.data.reverse());
    } catch (error) {
      console.error('Error fetching pokemons:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const pokeApiResponse = await axios.get(`https://pokeapi.co/api/v2/pokemon/${formData.pokedexNumber}`);
      const pokemonData = {
        name: pokeApiResponse.data.name.charAt(0).toUpperCase() + pokeApiResponse.data.name.slice(1),
        type: pokeApiResponse.data.types[0].type.name,
        image: pokeApiResponse.data.sprites.front_default,
        pokedexNumber: formData.pokedexNumber
      };
      setPreviewPokemon(pokemonData);
      setShowForm(false);
    } catch (error) {
      console.error('Error fetching pokemon:', error);
      alert('Pokemon not found! Please enter a valid Pokedex number (1-1010)');
    }
  };

  const confirmAddPokemon = async () => {
    try {
      await axios.post(`${API_URL}/pokemons`, previewPokemon);
      setPreviewPokemon(null);
      setFormData({ pokedexNumber: '' });
      fetchPokemons();
    } catch (error) {
      console.error('Error adding pokemon:', error);
    }
  };

  const rejectPokemon = () => {
    setPreviewPokemon(null);
    setFormData({ pokedexNumber: '' });
  };

  const goToNextPokemon = () => {
    const currentIndex = pokemons.findIndex(p => p.id === selectedPokemon.id);
    const nextIndex = (currentIndex + 1) % pokemons.length;
    setSelectedPokemon(pokemons[nextIndex]);
  };

  const goToPrevPokemon = () => {
    const currentIndex = pokemons.findIndex(p => p.id === selectedPokemon.id);
    const prevIndex = (currentIndex - 1 + pokemons.length) % pokemons.length;
    setSelectedPokemon(pokemons[prevIndex]);
  };

  const openNameEdit = () => {
    setNameEdit(selectedPokemon);
    setNewName(selectedPokemon.name);
  };

  const saveNewName = async () => {
    try {
      await axios.put(`${API_URL}/pokemons/${nameEdit.id}`, {
        ...nameEdit,
        name: newName
      });
      setNameEdit(null);
      setNewName('');
      fetchPokemons();
      setSelectedPokemon({...selectedPokemon, name: newName});
    } catch (error) {
      console.error('Error updating name:', error);
    }
  };

  const cancelNameEdit = () => {
    setNameEdit(null);
    setNewName('');
  };



  const handleDelete = async (id, name) => {
    setReleaseConfirm({ id, name });
  };

  const confirmRelease = async () => {
    try {
      await axios.delete(`${API_URL}/pokemons/${releaseConfirm.id}`);
      setReleaseConfirm(null);
      setSelectedPokemon(null);
      fetchPokemons();
    } catch (error) {
      console.error('Error releasing pokemon:', error);
    }
  };

  const cancelRelease = () => {
    setReleaseConfirm(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <img 
          src="https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pok%C3%A9mon_logo.svg" 
          alt="Pokemon Logo" 
          className="pokemon-logo"
        />
        <h1>Pokedex</h1>
        <button className="add-btn" onClick={() => setShowForm(!showForm)}>
          + Add Pokemon
        </button>
      </header>
      
      {showForm && (
        <form onSubmit={handleSubmit} className="pokemon-form">
          <input
            type="number"
            placeholder="Enter Pokedex Number (1-1010)"
            value={formData.pokedexNumber}
            onChange={(e) => setFormData({pokedexNumber: e.target.value})}
            min="1"
            max="1010"
            required
          />
          <button type="submit">
            Add Pokemon
          </button>
        </form>
      )}

      <div className="pokemon-grid">
        {pokemons.map(pokemon => (
          <div key={pokemon.id} className="pokemon-card" onClick={() => setSelectedPokemon(pokemon)}>
            {pokemon.image && (
              <img 
                src={pokemon.image} 
                alt={pokemon.name}
                className="pokemon-image"
                onError={(e) => e.target.style.display = 'none'}
              />
            )}
            <h3>{pokemon.name}</h3>
            <div className={`type-badge type-${pokemon.type.toLowerCase()}`}>{pokemon.type}</div>

          </div>
        ))}
      </div>

      {previewPokemon && (
        <div className="pokemon-modal" onClick={rejectPokemon}>
          <div className="preview-card" onClick={(e) => e.stopPropagation()}>
            <h3>Add this Pokemon?</h3>
            <div className="pokemon-preview">
              {previewPokemon.image && (
                <img 
                  src={previewPokemon.image} 
                  alt={previewPokemon.name}
                  className="pokemon-image"
                />
              )}
              <h4>{previewPokemon.name}</h4>
              <div className={`type-badge type-${previewPokemon.type.toLowerCase()}`}>{previewPokemon.type}</div>
            </div>
            <div className="preview-actions">
              <button className="accept-btn" onClick={confirmAddPokemon}>Accept</button>
              <button className="reject-btn" onClick={rejectPokemon}>Reject</button>
            </div>
          </div>
        </div>
      )}

      {nameEdit && (
        <div className="name-modal" onClick={cancelNameEdit}>
          <div className="name-edit-card" onClick={(e) => e.stopPropagation()}>
            <h3>Change Pokemon Name</h3>
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              className="name-input"
              maxLength="20"
            />
            <div className="name-actions">
              <button className="accept-btn" onClick={saveNewName}>Accept</button>
              <button className="reject-btn" onClick={cancelNameEdit}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {releaseConfirm && (
        <div className="name-modal" onClick={cancelRelease}>
          <div className="release-confirm-card" onClick={(e) => e.stopPropagation()}>
            <h3>Release Pokemon?</h3>
            <p>Are you sure you want to release <strong>{releaseConfirm.name}</strong>?</p>
            <p>This action cannot be undone.</p>
            <div className="name-actions">
              <button className="accept-btn" onClick={confirmRelease}>Release</button>
              <button className="reject-btn" onClick={cancelRelease}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {selectedPokemon && (
        <div className="pokemon-modal" onClick={() => setSelectedPokemon(null)}>
          <div className="pokedex-device" onClick={(e) => e.stopPropagation()}>
            <div className="pokedex-top">
              <div className="power-light"></div>
              <div className="small-lights">
                <div className="light red" onClick={() => setSelectedPokemon(null)}>×</div>
                <div className="light yellow"></div>
                <div className="light green"></div>
              </div>
            </div>
            <div className="pokedex-screen">
              <div className="screen-border">
                <div className="screen-content">
                  {selectedPokemon.image && (
                    <img 
                      src={selectedPokemon.image} 
                      alt={selectedPokemon.name}
                      className="pokemon-detail-image"
                    />
                  )}
                  <h2>{selectedPokemon.name}</h2>
                  <div className="pokemon-stats">
                    <div className="stat-row">
                      <span>Type:</span> <div className={`type-badge type-${selectedPokemon.type.toLowerCase()}`}>{selectedPokemon.type}</div>
                    </div>


                  </div>
                  <div className="description">
                    {selectedPokemon.description || 'A mysterious Pokemon with unique abilities.'}
                  </div>
                </div>
              </div>
            </div>
              <div className="pokedex-controls">
                <div className="control-pad">
                  <div className="dpad" onClick={goToPrevPokemon}>
                    <div className="dpad-center">←</div>
                  </div>
                  <div className="dpad" onClick={goToNextPokemon}>
                    <div className="dpad-center">→</div>
                  </div>
                </div>
                <div className="buttons">
                  <button className="btn-a" onClick={openNameEdit}>Name</button>
                  <button className="btn-b" onClick={() => handleDelete(selectedPokemon.id, selectedPokemon.name)}>Release</button>
                </div>
              </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
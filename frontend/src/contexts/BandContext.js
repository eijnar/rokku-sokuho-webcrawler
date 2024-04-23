import React, { createContext, useState, useEffect, useCallback } from 'react';
import { fetchBands, fetchBandUrls, addBand, deleteBand, updateBand, addUrl, updateUrl, deleteUrl } from '../services/api';

export const BandContext = createContext();

export const BandProvider = ({ children }) => {
    const [bands, setBands] = useState([]);
    const [urls, setUrls] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const initializeBands = async () => {
            const response = await fetchBands();
            setBands(response.data);
        };

        try {
            initializeBands();
        } catch (err) {
            setError('Failed to fetch bands');
            console.error(err);
        }
        setLoading(false);
    }, []);

    const fetchUrlsForBand = useCallback(async (bandId) => {
        if (!bandId || urls[bandId]) {
            console.log('No need to fetch or already fetched:', bandId);
            return;
        }
        try {
            const urlResponse = await fetchBandUrls(bandId);
            setUrls(prevUrls => ({
                ...prevUrls,
                [bandId]: urlResponse.data || []
            }));
        } catch (error) {
            console.error(`Failed to fetch URLs for band ${bandId}:`, error);
        }
    }, [urls]); 

    const handleAddUrl = async (bandId, urlData) => {
        const response = await addUrl(bandId, urlData);
        setUrls(prevUrls => ({
            ...prevUrls,
            [bandId]: [...prevUrls[bandId], response.data]
        }));
    };

    const handleUpdateUrl = async (bandId, urlId, newUrlData) => {
        const response = await updateUrl(urlId, newUrlData);
        const updatedUrls = urls[bandId].map(url => {
            if (url.id === urlId) return response.data;
            return url;
        });
        setUrls(prevUrls => ({
            ...prevUrls,
            [bandId]: updatedUrls
        }));
    };

    const handleDeleteUrl = async (bandId, urlId) => {
        await deleteUrl(urlId);
        const filteredUrls = urls[bandId].filter(url => url.id !== urlId);
        setUrls(prevUrls => ({
            ...prevUrls,
            [bandId]: filteredUrls
        }));
    };

    const handleAddBand = async (band) => {
        const response = await addBand(band);
        setBands(prevBands => [...prevBands, response.data]);
        setUrls(prevUrls => ({
            ...prevUrls,
            [response.data.id]: []
        }));
    };

    const handleDeleteBand = async (id) => {
        await deleteBand(id);
        setBands(bands.filter(band => band.id !== id));
        setUrls(prevUrls => {
            const updatedUrls = { ...prevUrls };
            delete updatedUrls[id];
            return updatedUrls;
        });
    };

    const handleUpdateBand = async (id, band) => {
        const response = await updateBand(id, band);
        const index = bands.findIndex(b => b.id === id);
        const updatedBands = [...bands];
        updatedBands[index] = response.data;
        setBands(updatedBands);
    };

    return (
        <BandContext.Provider value={{
            bands,
            urls,
            loading,
            error,
            addBand: handleAddBand,
            deleteBand: handleDeleteBand,
            updateBand: handleUpdateBand,
            addUrl: handleAddUrl,
            updateUrl: handleUpdateUrl,
            deleteUrl: handleDeleteUrl,
            fetchUrlsForBand,
        }}>
            {children}
        </BandContext.Provider>
    );
};
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;
const API_VERSION = process.env.REACT_APP_API_VERSION

/* URL section CRUD */
export const fetchBands = async () => {
    return await axios.get(`${API_URL}/${API_VERSION}/bands`);
};

export const addBand = async (band) => {
    return await axios.post(`${API_URL}/${API_VERSION}/bands`, band);
};

export const deleteBand = async (id) => {
    return await axios.delete(`${API_URL}/${API_VERSION}/bands/${id}`);
};

export const updateBand = async (id, band) => {
    return await axios.put(`${API_URL}/${API_VERSION}/bands/${id}`, band);
};

/* URL section CRUD */
export const fetchBandUrls = async (bandId) => {
    return await axios.get(`${API_URL}/${API_VERSION}/urls/?band_id=${bandId}`);
};

export const addUrl = async (url) => {
    return await axios.post(`${API_URL}/${API_VERSION}/urls/`, url);
};

export const updateUrl = async (id, urlData) => {
    return await axios.put(`${API_URL}/${API_VERSION}/urls/${id}`, urlData);
};

export const deleteUrl = async (id) => {
    return await axios.delete(`${API_URL}/${API_VERSION}/urls/${id}`);
};

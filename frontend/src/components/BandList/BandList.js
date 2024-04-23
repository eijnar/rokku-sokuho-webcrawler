import React, { useContext } from 'react';
import { BandContext } from '../../contexts/BandContext';
import BandCard from '../BandCard/BandCard';

const BandList = () => {
    const { bands } = useContext(BandContext);

    return (
        <div>
            <h1>Bands</h1>
            <div className="band-card-container">
                {bands.map(band => (
                    <BandCard key={band.band_id} bandId={band.band_id.toString()} />
                ))}
                
            </div>
        </div>
    );
};

export default BandList;
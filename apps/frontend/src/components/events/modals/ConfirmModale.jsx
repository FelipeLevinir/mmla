import React from 'react';
import styles from './confirmModal.module.css';

const ConfirmModal = ({ start, end, onConfirm, onCancel }) => {
  return (
    <div className={styles.modal}>
      <div className={styles.modalContent}>
        <h2>Confirmar Intervalo</h2>
        <p>
          Intervalo seleccionado: <strong>{start} - {end}</strong>
        </p>
        <p><strong>¿Deseas crear este intervalo?</strong></p>
        <div className={styles.buttonContainer}>
          <button className={styles.buttonAccept} onClick={onConfirm}>Aceptar</button>
          <button className={styles.buttonRefuse} onClick={onCancel}>Cancelar</button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;
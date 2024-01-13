import React, { useEffect, useState } from 'react';
import { Link, RouteComponentProps } from 'react-router-dom';
import NavigationLink from 'plaid-threads/NavigationLink';
import LoadingSpinner from 'plaid-threads/LoadingSpinner';

import { TransactionType } from './types';
import { useTransactions } from '../services';
import { setLabel } from '../services/api';

import { LoadingCallout, ErrorMessage } from '.';

// This page will focus solely on transactions for a user

const TransactionsPage = ({
  match,
}: RouteComponentProps<{ userId: string }>) => {
  const [userTransactions, setUserTransactions] = useState<TransactionType[]>(
    []
  );
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(0);
  const transactionsPerPage = 50;

  const { getTransactionsByUser, transactionsByUser } = useTransactions();
  const userId = Number(match.params.userId);

  useEffect(() => {
    // Initiates the fetching of transactions for the given user
    getTransactionsByUser(userId);
  }, [getTransactionsByUser, userId]);

  useEffect(() => {
    // fetches the transactions for the given user
    const fetchedTransactions = transactionsByUser[userId];
    if (fetchedTransactions) {
      if (fetchedTransactions.length > 0) {
        const sortedTransactions = [...fetchedTransactions].sort((a, b) => {
          // Type assertions
          const dateA = new Date(a.date as string);
          const dateB = new Date(b.date as string);
          return dateB.getTime() - dateA.getTime();
        });
        setUserTransactions(sortedTransactions);
      } else {
        setError('No transactions found.');
      }
    }
    setIsLoading(false);
  }, [transactionsByUser, userId]);

  // Calculate the visible transactions for the current page
  const indexOfLastTransaction = (currentPage + 1) * transactionsPerPage;
  const indexOfFirstTransaction = indexOfLastTransaction - transactionsPerPage;
  const currentTransactions = userTransactions.slice(
    indexOfFirstTransaction,
    indexOfLastTransaction
  );

  // Change page handler
  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  // Create label handler
  const handleLabelChange = async (transactionId: number, newLabel: any) => {
    try {
      await setLabel(transactionId, newLabel);
      const updatedTransactions = userTransactions.map(t =>
        t.id === transactionId ? { ...t, label: newLabel } : t
      );
      setUserTransactions(updatedTransactions);
    } catch (error) {
      // Handle error (e.g., show a notification or set an error state)
      console.error('Error updating label:', error);
    }
  };

  return (
    <div>
      <NavigationLink component={Link} to="/">
        BACK TO LOGIN
      </NavigationLink>
      <p />
      <NavigationLink component={Link} to={`/user/${userId}`}>
        USER SUMMARY
      </NavigationLink>

      <h1>User Transactions for ID: {userId}</h1>
      {isLoading ? (
        <div className="loading">
          <LoadingSpinner />
          <LoadingCallout />
        </div>
      ) : error ? (
        <ErrorMessage /> // Assuming ErrorMessage takes a 'message' prop
      ) : (
        <>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Account</th>
                <th>Amount</th>
                <th>Label</th>
                {/* Add other headers as needed */}
              </tr>
            </thead>
            <tbody>
              {currentTransactions.map((
                transaction // Use currentTransactions here
              ) => (
                <tr key={transaction.id}>
                  <td>{transaction.date.slice(0, 10)}</td>
                  <td>{transaction.name}</td>
                  <td>{transaction.account_id}</td>
                  <td>{transaction.amount}</td>
                  <td>
                    <input
                      type="text"
                      value={transaction.label}
                      onChange={e =>
                        handleLabelChange(transaction.id, e.target.value)
                      }
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="pagination">
            <button
              onClick={() => paginate(currentPage - 1)}
              disabled={currentPage === 0}
            >
              Previous
            </button>
            <button
              onClick={() => paginate(currentPage + 1)}
              disabled={indexOfLastTransaction >= userTransactions.length}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default TransactionsPage;

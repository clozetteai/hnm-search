import React, { createContext, useState, useContext, useEffect } from 'react';
import { ApiClient } from '../api/api'; // Update this path
import Cookies from 'js-cookie';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on component mount
    checkUserLoggedIn();
  }, []);

  const checkUserLoggedIn = async () => {
    try {
      const token = Cookies.get('token');
      if (token) {
        const userData = await ApiClient.getCurrentUser(token);
        setUser({ ...userData, token });
      }
    } catch (error) {
      console.error('Error checking user login status:', error);
      Cookies.remove('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      const data = await ApiClient.login(username, password);
      console.log(data)
      if (data.access_token) {
        Cookies.set('token', data.access_token);
        await checkUserLoggedIn(); // This will set the user state
        return true;
      } else {
        throw new Error('Login failed: No access token received');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const logout = () => {
    Cookies.remove('token');
    setUser(null);
  };

  const updateUser = async (settings) => {
    try {
      const token = Cookies.get('token');
      if (token) {
        const updatedUserData = await ApiClient.updateUserSettings(token, settings);
        setUser(prevUser => ({ ...prevUser, ...updatedUserData }));
      }
    } catch (error) {
      console.error('Error updating user settings:', error);
      throw error;
    }
  };

  const changePassword = async (currentPassword, newPassword, confirmNewPassword) => {
    try {
      const token = Cookies.get('token');
      if (token) {
        await ApiClient.changePassword(token, currentPassword, newPassword, confirmNewPassword);
        return true;
      }
    } catch (error) {
      console.error('Error changing password:', error);
      throw error;
    }
  };

  const value = {
    user,
    loading,
    login,
    logout,
    updateUser,
    changePassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
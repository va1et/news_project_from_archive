import React, { createContext, useState } from 'react';

export const MainContext = createContext();

export function MainContextProvider({ children }) {
  const [newsSelected, setNewsSelected] = useState(null);
  const [isNewsDrawerOpen, setIsNewsDrawerOpen] = useState(false);
  const [isEditDrawerOpen, setIsEditDrawerOpen] = useState(false);

  return (
    <MainContext.Provider
      value={{
        isNewsDrawerOpen,
        setIsNewsDrawerOpen,
        isEditDrawerOpen,
        setIsEditDrawerOpen,
        newsSelected,
        setNewsSelected,
      }}>
      {children}
    </MainContext.Provider>
  );
}

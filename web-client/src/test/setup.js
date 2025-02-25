import '@testing-library/jest-dom';

// Mock matchMedia for tests
window.matchMedia = window.matchMedia || function () {
    return {
        matches: false,
        addListener: function () { },
        removeListener: function () { }
    };
}; 
  // --------------------------------------------------------------------------
  /** Sort events by Frame */
  void EventList::sortPulseTime() const
  {
    // if (this->order == PULSETIME_SORT)
    //   return; // nothing to do

    // Avoid sorting from multiple threads
    Poco::ScopedLock<Mutex> _lock(m_sortMutex);
    // If the list was sorted while waiting for the lock, return.
    //if (this->order == PULSETIME_SORT)
    //  return;

    ... ...

  }

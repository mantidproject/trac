#ifndef DYNAMICFACTORY_H_
#define DYNAMICFACTORY_H_

//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Instantiator.h"
#include <map>

namespace Mantid
{
/** @class DynamicFactory DynamicFactory.h Kernel/DynamicFactory.h

    The dynmic factory is a base dynamic factory for serving up objects in response to requests from other classes.
    
    @author Nick Draper, Tessella Support Services plc
    @date 10/10/2007
    
    Copyright © 2007 ???RAL???

    This file is part of Mantid.

    Mantid is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    Mantid is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    File change history is stored at: <https://svn.mantidproject.org/mantid/trunk/Code/Mantid>    
*/
template <class Base>
class DynamicFactory
	/// A factory that creates objects by class name.
{
public:
	typedef AbstractInstantiator<Base> AbstractFactory;
	
	DynamicFactory()
		/// Creates the DynamicFactory.
	{
	}

	~DynamicFactory()
		/// Destroys the DynamicFactory and deletes the instantiators for 
		/// all registered classes.
	{
		for (typename FactoryMap::iterator it = _map.begin(); it != _map.end(); ++it)
		{
			delete it->second;
		}
	}
	
	Base* create(const std::string& className) const
		/// Creates a new instance of the class with the given name.
		/// The class must have been registered with registerClass.
		/// If the class name is unknown, a NotFoundException is thrown.
	{
		
		typename FactoryMap::const_iterator it = _map.find(className);
		if (it != _map.end())
			return it->second->createInstance();
		else
			throw NotFoundException(className);
	}
	
	template <class C> 
	void subscribe(const std::string& className)
		/// Registers the instantiator for the given class with the DynamicFactory.
		/// The DynamicFactory takes ownership of the instantiator and deletes
		/// it when it's no longer used.
		/// If the class has already been registered, an ExistsException is thrown
		/// and the instantiator is deleted.
	{
		registerClass(className, new Instantiator<C, Base>);
	}
	
	void subscribe(const std::string& className, AbstractFactory* pAbstractFactory)
		/// Registers the instantiator for the given class with the DynamicFactory.
		/// The DynamicFactory takes ownership of the instantiator and deletes
		/// it when it's no longer used.
		/// If the class has already been registered, an ExistsException is thrown
		/// and the instantiator is deleted.
	{
		std::auto_ptr<AbstractFactory> ptr(pAbstractFactory);
		typename FactoryMap::iterator it = _map.find(className);
		if (it == _map.end())
			_map[className] = ptr.release();
		else
			throw ExistsException(className);
	}
	
	void unsubscribe(const std::string& className)
		/// Unregisters the given class and deletes the instantiator
		/// for the class.
		/// Throws a NotFoundException if the class has not been registered.
	{
		typename FactoryMap::iterator it = _map.find(className);
		if (it != _map.end())
		{
			delete it->second;
			_map.erase(it);
		}
		else throw NotFoundException(className);
	}
	
	bool exists(const std::string& className) const
		/// Returns true if the given class is currently registered.
	{
		return _map.find(className) != _map.end();
	}
	

private:
	DynamicFactory(const DynamicFactory&);
	DynamicFactory& operator = (const DynamicFactory&);

	typedef std::map<std::string, AbstractFactory*> FactoryMap;
	
	FactoryMap _map;
};

}

#endif /*DYNAMICFACTORY_H_*/



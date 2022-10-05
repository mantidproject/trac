#ifndef INSTANTIATOR_H_
#define INSTANTIATOR_H_

namespace Mantid {
/** @class Instantiator Instantiator.h Kernel/Instantiator.h

    The instantiator is a generic clss for creating objects of the template type.

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
class AbstractInstantiator
	/// The common base class for all Instantiator instantiations.
	/// Used by DynamicFactory.
{
public:
	AbstractInstantiator()
		/// Creates the AbstractInstantiator.
	{
	}
	
	virtual ~AbstractInstantiator()
		/// Destroys the AbstractInstantiator.
	{
	}
	
	virtual Base* createInstance() const = 0;
		/// Creates an instance of a concrete subclass of Base.	

private:
	AbstractInstantiator(const AbstractInstantiator&);
	AbstractInstantiator& operator = (const AbstractInstantiator&);
};


template <class C, class Base>
class Instantiator: public AbstractInstantiator<Base>
	/// A template class for the easy instantiation of 
	/// instantiators. 
	///
	/// For the Instantiator to work, the class of which
	/// instances are to be instantiated must have a no-argument
	/// constructor.
{
public:
	Instantiator()
		/// Creates the Instantiator.
	{
	}
	
	virtual ~Instantiator()
		/// Destroys the Instantiator.
	{
	}

	Base* createInstance() const
	{
		return new C;
	}
};


}


#endif // INSTANTIATOR_H_

#ifndef MANTID_API_FADING_FRAME_H_
#define MANTID_API_FADING_FRAME_H_

#include "DllOption.h"

#include <QFrame>
#include <QColor>

class QWidget;

namespace MantidQt
{
namespace API
{
  /**
   * 
   *
   * Copyright &copy; 2014 ISIS Rutherford Appleton Laboratory & NScD Oak Ridge National Laboratory
   *
   * This file is part of Mantid.
   *
   * Mantid is free software; you can redistribute it and/or modify
   * it under the terms of the GNU General Public License as published by
   * the Free Software Foundation; either version 3 of the License, or
   * (at your option) any later version.
   *
   * Mantid is distributed in the hope that it will be useful,
   * but WITHOUT ANY WARRANTY; without even the implied warranty of
   * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   * GNU General Public License for more details.
   *
   * You should have received a copy of the GNU General Public License
   * along with this program.  If not, see <http://www.gnu.org/licenses/>.
   *
   * File change history is stored at: <https://github.com/mantidproject/mantid>
   * Code Documentation is available at: <http://doxygen.mantidproject.org>
   */
  class EXPORT_OPT_MANTIDQT_API FadingFrame : public QFrame
  {
    Q_OBJECT

  public:
    FadingFrame(QWidget * parent = 0);

    Q_PROPERTY(QColor fadeBorderColor READ fadeBorderColor WRITE setFadeBorderColor);
    Q_PROPERTY(QColor fadeBackgroundColor READ fadeBackgroundColor WRITE setFadeBackgroundColor);

    QColor fadeBorderColor() const { return m_fadeBorderColor; }
    QColor fadeBackgroundColor() const { return m_fadeBackgroundColor; }

    void setFadeBorderColor( const QColor & fadeBorderColor );
    void setFadeBackgroundColor( const QColor & fadeBackgroundColor );

    void doFadeAnimation();

  private:
    void setStyle(const QColor & borderColor, const QColor & backgroundColor);

    QColor m_fadeBorderColor;
    QColor m_fadeBackgroundColor;
  };


} // namespace API
} // namespace MantidQt

#endif  /* MANTID_API_FADING_FRAME_H_ */

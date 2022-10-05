#include "MantidQtAPI/FadingFrame.h"

#include <QByteArray>
#include <QEasingCurve>
#include <QParallelAnimationGroup>
#include <QPropertyAnimation>
#include <QWidget>

namespace // anonymous
{
  QPropertyAnimation * fade(QWidget * widget,
            int length,
            const QColor & normalColor,
            const QColor & fadeColor,
            const QByteArray & animationPropertyName)
  {
    QPropertyAnimation * animation = new QPropertyAnimation(widget, animationPropertyName);
    animation->setDuration(length);
    animation->setStartValue(fadeColor);
    animation->setEndValue(normalColor);
    animation->setEasingCurve(QEasingCurve::InExpo);
    return animation;
  }
} // anonymous namespace

namespace MantidQt
{
namespace API
{
  FadingFrame::FadingFrame(QWidget * parent) : QFrame(parent)
  {
    setFrameShape(QFrame::Panel);
    const QColor defaultColor = palette().color(QPalette::Background);
    setStyle(defaultColor, defaultColor);
  }
  
  void FadingFrame::setFadeBorderColor( const QColor & fadeBorderColor )
  {
    m_fadeBorderColor = fadeBorderColor;
  }

  void FadingFrame::setFadeBackgroundColor( const QColor & fadeBackgroundColor )
  {
    m_fadeBackgroundColor = fadeBackgroundColor;
    setStyle(m_fadeBorderColor, m_fadeBackgroundColor);
  }

  void FadingFrame::setStyle(const QColor & borderColor, const QColor & backgroundColor)
  {
    setStyleSheet("QLabel{ border-color     : " + borderColor.name() + ";"
                          "border-width     : 1px;"
                          "border-radius    : 3px;"
                          "border-style     : solid;"
                          "background-color : " + backgroundColor.name() + "; }");
  }

  void FadingFrame::doFadeAnimation()
  {
    static const QColor MANTID_GREEN = QColor(153,193,147);
    static const QColor BLACK = QColor(0,0,0);
    static const int LENGTH = 3000;

    QParallelAnimationGroup * group = new QParallelAnimationGroup(this);
    group->addAnimation(fade(this, LENGTH, palette().color(QPalette::Background), BLACK, "fadeBorderColor"));
    group->addAnimation(fade(this, LENGTH, palette().color(QPalette::Background), MANTID_GREEN, "fadeBackgroundColor"));
    group->start();
  }

} // namespace MantidQt
} // namespace API
